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
df = pd.read_sql('SELECT * FROM practice', con=con)
fig = px.scatter(df,
                 'LONGITUDE',
                 'LATITUDE',
                 color='SNOW',
                 size='ELEVATION',
                 hover_name='CITY',
                 height=1000,
                 width=1600)

# add oregon trace to scatter plot
fig.add_trace(fig_poly.data[0])

# create a consistent view of the entire state of oregon
fig.update_layout(yaxis_range=[41.75, 46.5],
                  xaxis_range=[-124.75, -116.25])


# initiate app
app = dash.Dash(__name__)


app.layout = html.Div(
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
    Input('location-dropdown', 'value'))
def update_map(location):


    # TODO: come back to this later to make call within callback statement after thread location is ignored
    # locs = ', '.join('"' + l + '"' for l in location)
    # query = 'SELECT o.SNOW, l.LONGITUDE, l.LATITUDE, l.ELEVATION, l.CITY FROM observations AS o JOIN locations AS l WHERE l.CITY IN (%s)' % locs
    # filtered_df = pd.read_sql(query, con=conn)

    filtered_df = df[df.CITY.isin(location)]

    fig = px.scatter(filtered_df,
                     'LONGITUDE',
                     'LATITUDE',
                     color='SNOW',
                     size='ELEVATION',
                     hover_name='CITY',
                     height=1000,
                     width=1600)

    # add trace of oregon
    fig.add_trace(fig_poly.data[0])

    # create a consistent view of the entire state of oregon
    fig.update_layout(yaxis_range=[41.75, 46.5],
                      xaxis_range=[-124.75, -116.25])

    return fig

# TODO: add ability to select date to filter map


# run app
if __name__ == '__main__':
    app.run_server(debug=True)



# TODO: what we will want to do is select and join where date = criteria

# TODO: allow user to select their location of interest

