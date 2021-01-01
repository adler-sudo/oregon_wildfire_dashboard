import plotly.express as px
from shapely.geometry import Polygon
import requests


# state polygon preparation
# make call to api for oregon coordinates
response = requests.get("https://services2.arcgis.com/DEoxb4q3EJppiDKC/arcgis/rest/services/States_shapefile/FeatureServer/0/query?where=State_Name%20%3D%20'OREGON'&outFields=*&outSR=4326&f=json")
coords = response.json()['features'][0]['geometry']['rings'][0]
poly = Polygon(coords)
x, y = poly.exterior.xy

# prep oregon state polygon
fig_poly = px.line(x=x, y=y, color_discrete_sequence=px.colors.qualitative.G10)

# base oregon plot
fig = px.scatter(height=1000,
                 width=1600)
fig.update_layout(plot_bgcolor='rgb(180, 180, 180)')
fig.add_trace(fig_poly.data[0])
# create a consistent view of the entire state of oregon
fig.update_layout(yaxis_range=[41.75, 46.5],
                  xaxis_range=[-124.75, -116.25])


# TODO: consolidate database calls so that tables can be imported (make this a class?)