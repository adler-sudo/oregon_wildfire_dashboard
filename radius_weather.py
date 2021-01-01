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

# import master app
from app import app

# import base_objects
from base_objects import fig


# sqlite3 method
con = sqlite3.connect("weatherData.db")

# only bringing in portion of data since whole dataset is too large for pycharm right now
query = 'SELECT DISTINCT CITY FROM locations'
loc_exec = con.execute(query)
loc_exec = loc_exec.fetchall()
locations = [l for l, in loc_exec]
locations.sort()

# state polygon preparation
# make call to api for oregon coordinates
response = requests.get("https://services2.arcgis.com/DEoxb4q3EJppiDKC/arcgis/rest/services/States_shapefile/FeatureServer/0/query?where=State_Name%20%3D%20'OREGON'&outFields=*&outSR=4326&f=json")
coords = response.json()['features'][0]['geometry']['rings'][0]
poly = Polygon(coords)
x, y = poly.exterior.xy

# prep oregon state polygon
fig_poly = px.line(x=x, y=y, color_discrete_sequence=px.colors.qualitative.G10)

# initiate scatter
colorscale = 'ice_r'
min_prcp = 0
max_prcp = 1.5
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
            id='radius-weather-location-dropdown',
            options=[
                {'label': l, 'value': l} for l in locations
            ],
            multi=False,
            value=locations[0],
        ),
        dcc.DatePickerRange(
            id='radius-weather-datepicker-range',
            start_date=date(2019, 12, 23),
            end_date=date(2019, 12, 23)
        ),
        dcc.Graph(
            id='radius-weather-map',
            figure=fig
        )
    ]
)

# location-specific map
# will want this to eventually include locations within a given region
@app.callback(
    Output('radius-weather-map', 'figure'),
    Output('radius-weather-location-dropdown', 'options'),
    [Input('radius-weather-location-dropdown', 'value'),
     Input('radius-weather-datepicker-range', 'start_date'),
     Input('radius-weather-datepicker-range', 'end_date')])
def update_map(location, start_date, end_date):

    # connect to database and pull data only within timeframe
    con = sqlite3.connect("weatherData.db")
    query = 'SELECT o.NAME, o.DATE, o.PRCP, l.CITY, l.LATITUDE, l.LONGITUDE, l.ELEVATION ' \
            'FROM observations AS o ' \
            'JOIN locations AS l ' \
            'ON o.NAME = l.CITY ' \
            'WHERE o.DATE >= ? AND o.DATE <= ?'
    df = pd.read_sql(query, con=con, parse_dates=['DATE'], params=[start_date, end_date])
    df.fillna({'PRCP': 0}, inplace=True)

    latitude = df.loc[df.CITY == location, 'LATITUDE'].iloc[0]
    longitude = df.loc[df.CITY == location, 'LONGITUDE'].iloc[0]
    filtered_df = df.loc[(df.LATITUDE > latitude - 1) & (df.LATITUDE < latitude + 1)]
    filtered_df = filtered_df.loc[(filtered_df.LONGITUDE > longitude - 1) & (filtered_df.LONGITUDE < longitude + 1)]

    # average over date range
    for l in filtered_df.CITY.unique():
        filtered_df.loc[filtered_df.CITY == l, 'PRCP'] = filtered_df.groupby('CITY')['PRCP'].mean()[l]

    # recreate figure
    # check for empty dataframe
    if len(filtered_df) > 0:
        fig = px.scatter(filtered_df,
                         'LONGITUDE',
                         'LATITUDE',
                         color='PRCP',
                         color_continuous_scale=colorscale,
                         range_color=[min_prcp, max_prcp],
                         hover_name='CITY',
                         height=1000,
                         width=1600,
                         render_mode='webgl')
    else:
        fig = px.scatter(height=1000,
                         width=1600)

    # outline markers
    fig.update_traces(marker=dict(line=dict(width=1, color='Black'), size=10))

    # add trace of oregon
    fig.add_trace(fig_poly.data[0])

    # create a consistent view of the entire state of oregon
    fig.update_layout(yaxis_range=[41.75, 46.5],
                      xaxis_range=[-124.75, -116.25],
                      plot_bgcolor='rgb(180, 180, 180)')

    locations = df.CITY.unique()
    locations.sort()
    new_locations = [
        {'label': l, 'value': l} for l in locations
    ]
    return fig, new_locations





# TODO: what we will want to do is select and join where date = criteria

# TODO: allow user to select their location of interest

