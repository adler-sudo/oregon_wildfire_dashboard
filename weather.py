from sqlalchemy import Table, MetaData, create_engine, select
import pandas as pd
from sqlalchemy.orm import sessionmaker
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from shapely.geometry import Polygon
import requests
from dash.dependencies import Output, Input
import numpy as np
import sqlite3

# date modules
from datetime import date
import datetime

# import master app
from firesByYear import app

# import base objects
from base_objects import fig


# TODO: need to go in and switch this initial df/fig to come from weatherData
# convert fire database to dataframe
# sqlalcehmy method
# engine = create_engine('sqlite:///practiceWeather.db')
# conn = engine.connect()
# metadata = MetaData()

# sqlite3 method
con = sqlite3.connect("practiceWeather.db")

# select weather table
# observations = select([Table('observations', metadata, autoload=True, autoload_with=engine)])
# locations = select([Table('locations', metadata, autoload=True, autoload_with=engine)])
# weatherQuery = observations.join(locations, observations.c.NAME == locations.c.name)
# recordsGeo = conn.execute(weatherQuery).fetchall()
#
# dfGeo = pd.DataFrame(recordsGeo, columns=weather.columns.keys())
# dfGeo.drop(columns=['index'], inplace=True)
# dfGeo.dropna(subset=['total_acres'], inplace=True)

# select locations table

# TODO: need to switch this to come from weather data and pick a specific day
# extract locations list
query = 'SELECT NAME FROM practice ORDER BY NAME'
locations = con.execute(query).fetchall()
locations = [l for l, in locations]
locations = list(set(locations))

# extract dates list
query = 'SELECT DATE FROM practice ORDER BY NAME'
dates = con.execute(query).fetchall()
dates = [d for d, in dates]
dates = list(set(dates))

# state polygon preparation
# make call to api for oregon coordinates
response = requests.get("https://services2.arcgis.com/DEoxb4q3EJppiDKC/arcgis/rest/services/States_shapefile/FeatureServer/0/query?where=State_Name%20%3D%20'OREGON'&outFields=*&outSR=4326&f=json")
coords = response.json()['features'][0]['geometry']['rings'][0]
poly = Polygon(coords)
x, y = poly.exterior.xy

# prep oregon state polygon
fig_poly = px.line(x=x, y=y, color_discrete_sequence=px.colors.qualitative.G10)

# right now just set up to use single day from practice data since
# primary database is so large
df = pd.read_sql('SELECT * FROM practice', con=con, parse_dates=['DATE'])

# filling prcp na with 0 (may want to look at different method moving forward?) - could sway data
df.fillna({'PRCP':0}, inplace=True)

# initiate plot
colorscale = 'blues'
min_prcp = df.groupby('NAME')['PRCP'].mean().min()
max_prcp = df.groupby('NAME')['PRCP'].mean().max()
fig = fig

# add oregon trace to scatter plot
fig.add_trace(fig_poly.data[0])

# create a consistent view of the entire state of oregon
fig.update_layout(yaxis_range=[41.75, 46.5],
                  xaxis_range=[-124.75, -116.25])

# define layout
layout = html.Div(
    children=[
        dcc.Dropdown(
            id='location-dropdown',
            options=[
                {'label': l, 'value': l} for l in locations
            ],
            multi=True,
            value=np.array(locations),
            style={
                'height': '50vh',
                'overflow-y': 'scroll'
            }
        ),
        dcc.DatePickerRange(
            id='datepicker-range',
            start_date=date(2019, 12, 23),
            end_date=date(2019, 12, 23)
        ),
        dcc.Graph(
            id='weather-map',
            figure=fig
        )
    ]
)

# location-specific map
# will want this to eventually include locations within a given region
@app.callback(
    Output('weather-map', 'figure'),
    [Input('location-dropdown', 'value'),
     Input('datepicker-range', 'start_date'),
     Input('datepicker-range', 'end_date')])
def update_map(location, start_date, end_date):


    # TODO: come back to this later to make call within callback statement after thread location is ignored
    # locs = ', '.join('"' + l + '"' for l in location)
    # query = 'SELECT o.SNOW, l.LONGITUDE, l.LATITUDE, l.ELEVATION, l.CITY FROM observations AS o JOIN locations AS l WHERE l.CITY IN (%s)' % locs
    # filtered_df = pd.read_sql(query, con=conn)

    # filter by selected locations
    filtered_df = df[df.CITY.isin(location)]

    # filter by selected date range
    filtered_df = filtered_df[(filtered_df.DATE >= start_date) & (filtered_df.DATE <= end_date)]

    # TODO: may need to look at speeding this up a bit (can i remove loop, can i be more efficient in slicing)
    # average over date range
    for l in filtered_df.NAME.unique():
        filtered_df.loc[filtered_df.NAME == l, 'PRCP'] = filtered_df.groupby('NAME')['PRCP'].mean()[l]

    # recreate figure
    fig = px.scatter(filtered_df,
                     'LONGITUDE',
                     'LATITUDE',
                     color='PRCP',
                     color_continuous_scale=colorscale,
                     range_color=[min_prcp, max_prcp],
                     size='PRCP',
                     hover_name='CITY',
                     height=1000,
                     width=1600)

    # add marker border
    fig.update_traces(marker=dict(line=dict(width=2, color='Black')))

    # add trace of oregon
    fig.add_trace(fig_poly.data[0])

    # create a consistent view of the entire state of oregon
    fig.update_layout(yaxis_range=[41.75, 46.5],
                      xaxis_range=[-124.75, -116.25],
                      plot_bgcolor='rgb(180, 180, 180)')

    return fig





# TODO: what we will want to do is select and join where date = criteria

# TODO: allow user to select their location of interest

