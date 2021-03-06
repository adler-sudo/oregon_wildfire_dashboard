# import dash packages
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# import plotly
import plotly.express as px
import plotly

# import data handling packages
import pandas as pd
from sqlalchemy import (create_engine,
                        select,
                        Table,
                        MetaData)

# import app
from app import app

# import base objects
from base_objects import fig, fig_poly


# convert fire database to dataframe
engine = create_engine('sqlite:///fire.db')
conn = engine.connect()
metadata = MetaData()


# select geo table
geo = Table('geo', metadata, autoload=True, autoload_with=engine)
queryGeo = select([geo])
recordsGeo = conn.execute(queryGeo).fetchall()
dfGeo = pd.DataFrame(recordsGeo, columns=geo.columns.keys())
dfGeo.drop(columns=['index'], inplace=True)
dfGeo.dropna(subset=['total_acres'], inplace=True)

# define explicit color map for each general cause
# TODO: will want to define this as a global variable that can be used in each page
causes = dfGeo['general_cause'].unique()
colors = plotly.colors.qualitative.Vivid
color_map = {cause: colors[n] for n, cause in enumerate(causes)}

# construct page layout
layout = html.Div(
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
                     color_discrete_map=color_map,
                     size='total_acres',
                     height=1000,
                     width=1600)

    # alter marker size to display ratio ref, but also represent each fire (ie small ones still represented)
    fig.update_traces(marker_sizeref=dfGeo['total_acres'].max() / 200 ** 2,
                      marker_sizemin=3,
                      marker=dict(line=dict(width=1, color='Black')))

    # create a consistent view of the entire state of oregon
    fig.update_layout(yaxis_range=[41.75, 46.5],
                      xaxis_range=[-124.75, -116.25],
                      plot_bgcolor='rgb(180, 180, 180)')
    # add oregon boundary trace
    fig.add_trace(fig_poly.data[0])

    return fig



# TODO: allow user to select their location of interest and display fires within a 50 mile radius
# TODO: include weather and fire data in the same view. filter by 50 mile radius.



