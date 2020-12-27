from sqlalchemy import Table, MetaData, create_engine, select
import pandas as pd
from sqlalchemy.orm import sessionmaker
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from shapely.geometry import Polygon
import requests



# convert fire database to dataframe
engine = create_engine('sqlite:///practiceWeather.db')
conn = engine.connect()
metadata = MetaData()

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
df = pd.read_sql('SELECT * FROM practice', con=conn)
fig = px.scatter(df,
                 'LONGITUDE',
                 'LATITUDE',
                 color='PRCP',
                 size='PRCP',
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
        dcc.Graph(
            figure=fig
        )
    ]
)



if __name__ == '__main__':
    app.run_server(debug=True)



# TODO: what we will want to do is select and join where date = criteria

# TODO: allow user to select their location of interest

