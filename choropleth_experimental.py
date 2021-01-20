
# additional packages needed
import dash_html_components as html
import dash_core_components as dcc




# choropleth code directly from plortly example (believe this is same as virginia tutorial)
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

df = df.loc[df.fips.str[:2] == '41']

import plotly.express as px

fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                    color_continuous_scale="purples",
                    range_color=(0, 12),
                    labels={'unemp': 'unemployment rate'}
                    )
fig.update_geos(fitbounds='locations',
                visible=False)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})



# define layout
layout = html.Div(
    children=[
        dcc.Graph(
            figure=fig
        )
    ]
)
