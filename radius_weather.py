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
from base_objects import fig, fig_poly


# sqlite3 method
con = sqlite3.connect("weatherData.db")

# only bringing in portion of data since whole dataset is too large for pycharm right now
query = 'SELECT DISTINCT CITY FROM locations'
loc_exec = con.execute(query)
loc_exec = loc_exec.fetchall()
locations = [l for l, in loc_exec]
locations.sort()

# define types of analysis
analysis_types = ['EVAP', 'PRCP', 'SNOW', 'TAVG', 'TMAX', 'TMIN']

# initiate scatter
colorscale = 'ice_r'
min_prcp = 0
max_prcp = 1.5

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
        dcc.Dropdown(
            id='analysis-type-selector',
            options=[
                {'label': a, 'value': a} for a in analysis_types
            ],
            value='PRCP'
        ),
        dcc.Loading(
            id='loading-2',
            type='default',
            children=html.Div(id='loading-output-2')
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
    Output('loading-output-2', 'children'),
    [Input('radius-weather-location-dropdown', 'value'),
     Input('radius-weather-datepicker-range', 'start_date'),
     Input('radius-weather-datepicker-range', 'end_date'),
     Input('analysis-type-selector', 'value')])
def update_map(location, start_date, end_date, analysis_type):

    # connect to database and pull data only within timeframe
    con = sqlite3.connect("weatherData.db")
    columns = ['o.NAME', 'o.DATE', analysis_type, 'l.CITY', 'l.LATITUDE', 'l.LONGITUDE']

    # TODO: define data types when reading in dataframe (category, float16)
    query = 'SELECT %s ' \
            'FROM observations AS o ' \
            'JOIN locations AS l ' \
            'ON o.NAME = l.CITY ' \
            'WHERE o.DATE >= ? AND o.DATE <= ?' % ','.join(columns)
    df = pd.read_sql(query, con=con, parse_dates=['DATE'], params=[start_date, end_date])
    df.fillna({analysis_type: 0}, inplace=True)

    latitude = df.loc[df.CITY == location, 'LATITUDE'].iloc[0]
    longitude = df.loc[df.CITY == location, 'LONGITUDE'].iloc[0]
    filtered_df = df.loc[(df.LATITUDE > latitude - 1) & (df.LATITUDE < latitude + 1)]
    filtered_df = filtered_df.loc[(filtered_df.LONGITUDE > longitude - 1) & (filtered_df.LONGITUDE < longitude + 1)]

    # average over date range
    for l in filtered_df.CITY.unique():
        filtered_df.loc[filtered_df.CITY == l, analysis_type] = filtered_df.groupby('CITY')[analysis_type].mean()[l]

    # drop 0 rows
    filtered_df = filtered_df.loc[filtered_df[analysis_type] != 0]

    # recreate figure
    # check for empty dataframe
    if len(filtered_df) > 0:
        fig = px.scatter(filtered_df,
                         'LONGITUDE',
                         'LATITUDE',
                         color=analysis_type,
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

    # loading animation
    summary = ''

    return fig, new_locations, summary





# TODO: what we will want to do is select and join where date = criteria

# TODO: allow user to select their location of interest

