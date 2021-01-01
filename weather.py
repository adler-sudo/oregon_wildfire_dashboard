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
from base_objects import fig, fig_poly

# loading packages
import time


# sqlite3 method
con = sqlite3.connect("weatherData.db")

# get locations
query = 'SELECT DISTINCT CITY FROM locations'
loc_exec = con.execute(query)
loc_exec = loc_exec.fetchall()
locations = [l for l, in loc_exec]
locations.sort()

# define types of analysis
analysis_types = ['EVAP', 'PRCP', 'SNOW', 'TAVG', 'TMAX', 'TMIN']

# initiate plot
colorscale = 'blues'

# TODO: need to move these back to dynamic now that we have all weather data available
min_prcp = 0
max_prcp = 1.5

# define layout
layout = html.Div(
    children=[
        dcc.DatePickerRange(
            id='datepicker-range',
            start_date=date(2019, 12, 23),
            end_date=date(2019, 12, 23)
        ),
        dcc.Dropdown(
            id='analysis-type-selector',
            options=[
                {'label': a, 'value': a} for a in analysis_types
            ],
            value='PRCP'
        ),
        dcc.Loading(
            id='loading-1',
            type='default',
            children=html.Div(id='loading-output-1')
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
    Output('loading-output-1', 'children'),
    [Input('datepicker-range', 'start_date'),
     Input('datepicker-range', 'end_date'),
     Input('analysis-type-selector', 'value')])
def update_map(start_date, end_date, analysis_type):

    # connect to database and pull data only within timeframe
    con = sqlite3.connect("weatherData.db")
    columns = ('o.NAME', 'o.DATE', analysis_type, 'l.CITY', 'l.LATITUDE', 'l.LONGITUDE')
    query = 'SELECT %s ' \
            'FROM observations AS o ' \
            'JOIN locations AS l ' \
            'ON o.NAME = l.CITY ' \
            'WHERE o.DATE >= ? AND o.DATE <= ?' % ','.join(columns)

    filtered_df = pd.read_sql(query, con=con, parse_dates=['DATE'], params=[start_date, end_date])

    # filter by selected locations
    filtered_df.fillna({analysis_type: 0}, inplace=True)

    # average over date range
    for l in filtered_df.CITY.unique():
        filtered_df.loc[filtered_df.CITY == l, analysis_type] = filtered_df.groupby('CITY')[analysis_type].mean()[l]

    # drop 0 rows
    filtered_df = filtered_df.loc[filtered_df[analysis_type] != 0]

    # recreate figure
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

    # outline markers
    fig.update_traces(marker=dict(line=dict(width=1, color='Black'), size=12))

    # add trace of oregon
    fig.add_trace(fig_poly.data[0])

    # create a consistent view of the entire state of oregon
    fig.update_layout(yaxis_range=[41.75, 46.5],
                      xaxis_range=[-124.75, -116.25],
                      plot_bgcolor='rgb(180, 180, 180)')

    summary = ''

    return fig, summary





# TODO: what we will want to do is select and join where date = criteria

# TODO: allow user to select their location of interest

