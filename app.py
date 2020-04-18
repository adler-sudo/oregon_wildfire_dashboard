# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:05:02 2020

@author: james
"""

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


# convert fire database to dataframe
engine = create_engine('sqlite:///fire.db')
conn = engine.connect()
metadata = MetaData()

fires = Table('fires', metadata, autoload=True, autoload_with=engine)
geo = Table('geo', metadata, autoload=True, autoload_with=engine)

query = select([fires])
queryGeo = select([geo])

records = conn.execute(query).fetchall()
recordsGeo = conn.execute(queryGeo).fetchall()

df = pd.DataFrame(records, columns=fires.columns.keys())
dfGeo = pd.DataFrame(recordsGeo, columns=geo.columns.keys())

df.drop(columns=['index'], inplace=True)
dfGeo.drop(columns=['index'], inplace=True)
dfGeo.dropna(subset=['total_acres'], inplace=True)

df[df.general_cause.isnull()] = 'Miscellaneous'
df = df[df.fire_year != 'Miscellaneous']
df['fire_year'] = df.fire_year.astype(int)

# initiate app
app = dash.Dash(__name__)

colors = {
    'background': '#483C32',
    'text': '#B5EAAA',
}

# prepare components for stacked bar
stacked_df = df
causes = stacked_df.general_cause.unique()
fire_years = stacked_df.fire_year.unique()
graphs = []
plotColors = plotly.colors.qualitative.Alphabet

# create the total acres burned graph by general cause
for i in range(len(causes)):
    bar = go.Bar(name='{}'.format(causes[i]), x=list(stacked_df.fire_year.unique()),
                     y=list(stacked_df[stacked_df.general_cause == causes[i]].groupby('fire_year')['total_acres'].sum()),
                     marker_color=plotColors[i]
                     )
    graphs.append(bar)
    
fig = go.Figure(data=graphs)
fig.update_layout(barmode='stack',
                  title='Oregon Acres Burned by Cause by Year',
                  xaxis={'title':'Year'},
                  yaxis={'title':'Total Acres Burned'},
                  plot_bgcolor='#C3FBD8',
                  paper_bgcolor='#483C32',
                  font={'color':'#B5EAAA'},
                  )


countGraphs = []

# create the stacked count graph by general cause
for i in range(len(causes)):
    bar = go.Bar(name='{}'.format(causes[i]),
                 x=list(stacked_df.fire_year.unique()),
                 y=list(stacked_df[stacked_df.general_cause == causes[i]].groupby('fire_year')['general_cause'].count()),
                 marker_color=plotColors[i]
                 )
    countGraphs.append(bar)

countGraph = go.Figure(data=countGraphs)
countGraph.update_layout(barmode='stack',
                         title='Oregon Fire Count by Cause by Year',
                         xaxis={'title':'Year'},
                         yaxis={'title':'Total Count of Fires'},
                         plot_bgcolor='black',
                         paper_bgcolor='#483C32',
                         font={'color':'#B5EAAA'},
                         )



# set app layout
app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[
                                html.H1(
                                    children='Oregon Wildfire Dashboard',
                                    style={
                                        'textAlign': 'left',
                                        'color': colors['text']
                                    }
                                ),
                            
                                # the main body
                                html.Div(
                                    id='description',
                                    children='A page for Oregon wildfire data visualization.', style={
                                    'textAlign': 'left',
                                    'color': colors['text']
                                }),
                                
                                html.Div(id='theGraphsDiv',
                                         className='theGraphsClass',
                                         children=[
                                                html.Div(id='stackedDiv',
                                                         children=[
                                                             dcc.Graph(id='stackedGraph',
                                                                       figure=fig
                                                             )
                                                        ]
                                                ),
                                                html.Div(id='countDiv',
                                                         children=[
                                                             dcc.Graph(id='countGraph',
                                                                       figure=countGraph)
                                                             ]
                                                )
                                            ]
                                )
                            
                        ]
                )



if __name__ == '__main__':
    app.run_server(debug=True)
