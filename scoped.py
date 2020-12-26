# import dash packages
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly


# import data handling packages
import pandas as pd
from sqlalchemy import (create_engine,
                        select,
                        Table,
                        MetaData)

# modules needed for state polygon creation
import json
import requests
from shapely.geometry import Polygon

# convert fire database to dataframe
engine = create_engine('sqlite:///fire.db')
conn = engine.connect()
metadata = MetaData()

# TODO: create consistent color for fire cause across all plots

# select geo table
geo = Table('geo', metadata, autoload=True, autoload_with=engine)
queryGeo = select([geo])
recordsGeo = conn.execute(queryGeo).fetchall()
dfGeo = pd.DataFrame(recordsGeo, columns=geo.columns.keys())
dfGeo.drop(columns=['index'], inplace=True)
dfGeo.dropna(subset=['total_acres'], inplace=True)

# initialize plot
fig = px.scatter()

# state polygon preparation
# make call to api for oregon coordinates
response = requests.get("https://services2.arcgis.com/DEoxb4q3EJppiDKC/arcgis/rest/services/States_shapefile/FeatureServer/0/query?where=State_Name%20%3D%20'OREGON'&outFields=*&outSR=4326&f=json")
coords = response.json()['features'][0]['geometry']['rings'][0]
poly = Polygon(coords)
x, y = poly.exterior.xy

# plot the state polygon
fig_poly = px.line(x=x, y=y, color_discrete_sequence=px.colors.qualitative.G10)

# initiate app
app = dash.Dash(__name__)


# construct page layout
app.layout = html.Div(
    children=[
        dcc.Slider(
            id='year-slider',
            min=dfGeo['fire_year'].min(),
            max=dfGeo['fire_year'].max(),
            value=dfGeo['fire_year'].min(),
            marks={str(year): str(year) for year in dfGeo['fire_year'].unique()},
            step=None
        ),
        dcc.Graph(
            id='fire-geo-visualization',
            figure=fig
        ),
    ]
)

# filter by year
@app.callback(
    Output('fire-geo-visualization', 'figure'),
    Input('year-slider', 'value'))
def update_graph(selected_year):

    # filter for selected year
    filtered_df = dfGeo[dfGeo.fire_year == selected_year]

    # plot fires for selected year
    fig = px.scatter(filtered_df,
                     x='longitude',
                     y='latitude',
                     color='general_cause',
                     size='total_acres',
                     height=1000,
                     width=1600)
    fig.update_traces(marker_sizeref=dfGeo['total_acres'].max() / 200 ** 2,
                      marker_sizemin=3)
    fig.update_layout(yaxis_range=[41.75, 46.5],
                      xaxis_range=[-124.75, -116.25])
    # add oregon boundary trace
    fig.add_trace(fig_poly.data[0])

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)