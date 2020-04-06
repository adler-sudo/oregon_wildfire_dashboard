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

# import plotly components
import plotly.express as px


# import data handling packages
import pandas as pd
from sqlalchemy import (create_engine,
                        select,
                        Table,
                        MetaData)
import numpy as np

# convert database to dataframe
engine = create_engine('sqlite:///fire.db')
conn = engine.connect()
metadata = MetaData()
fires = Table('fires', metadata, autoload=True, autoload_with=engine)
query = select([fires])
records = conn.execute(query).fetchall()
df = pd.DataFrame(records, columns=fires.columns.keys())
df.drop(columns=['index'], inplace=True)
df[df.general_cause.isnull()] = 'Miscellaneous'
df = df[df.fire_year != 'Miscellaneous']
df['fire_year'] = df.fire_year.astype(int)


x = df.fire_year.unique()
y = df.groupby('fire_year')['total_acres'].sum()






lightning = df[df.general_cause == 'Smoking']
x_lightning = lightning.fire_year.unique()
y_lightning = lightning.groupby('fire_year')['total_acres'].sum()


# load in stylesheet


# initiate app
app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}







app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Oregon Wildfire Dashboard',
        style={
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Div(children='A page for Oregon wildfire data visualization.', style={
        'textAlign': 'left',
        'color': colors['text']
    }),

    dcc.Graph(
        id='total_acres_burned',
        figure={
            'data': [
                {'x': x,
                 'y': y,
                 'type': 'bar'}
                
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title': 'Total Acres Burned by Year',
                'xaxis':{
                    'title':'Year'
                },
                'yaxis':{
                    'title':'Acres Burned'
                }
            }
        }
    ),
  
    
    dcc.Dropdown(
        id='cause_dropdown',
        options=[{'label': i, 'value': i} for i in df.general_cause.unique()],
        value='Lightning'
    ),
        
        
    html.Div(id='dynamicBarSet',
             className='dynamicBarSet',
             children=[
    
    dcc.Graph(
        id='dynamic_graph',
    ),
    
    
    dcc.RangeSlider(
        id='my_range_slider',
        min=min(df.fire_year),
        max=max(df.fire_year),
        step=1,
        marks={
            1961: '1961',
            1970: '1970',
            1980: '1980',
            1990: '1990',
            2000: '2000',
            2010: '2010',
            2019: '2019'
        },
        value=[2010, 2019]
    ),
            ]
    ),
    
    
    html.Div(id='pieParent',
             className='pieParent',
             children=[
    
    html.Div(id='divYear',
             className='year',
             children=[
                dcc.Graph(
                    id='piechartYear'
                ),
                
                dcc.Dropdown(
                    id='piechartInput',
                    options=[{'label': i, 'value': i} for i in df.fire_year.unique()],
                    value=2019
                )
            ]
    ),
    
    html.Div(id='divCounty',
             className='county',
             children=[
                dcc.Graph(
                    id='piechartCounty'
                ),
                
                dcc.Dropdown(
                    id='piechartCountyInput',
                    options=[{'label': i, 'value': i} for i in df.fire_year.unique()],
                    value=2019
                )
            ]
    ),


    html.Div(id='divRedundant',
             className='redundant',
             children=[
                dcc.Graph(
                    id='piechartRedundant'
                ),
                dcc.Dropdown(
                    id='piechartRedundantInput',
                    options=[{'label': i, 'value': i} for i in df.general_cause.unique()],
                    value='Smoking'
                )
              ]
    )
            ]
    )
])






# app callback for dynamic bar graph
@app.callback(
    Output(component_id='dynamic_graph', component_property='figure'),
    [Input(component_id='cause_dropdown', component_property='value'),
     Input('my_range_slider', 'value')])
def update_output_div(cause, year):
    filtered_df = df[df.general_cause == cause]
    
    mask = (filtered_df.fire_year >= year[0]) & (filtered_df.fire_year <= year[1])
    filtered_df = filtered_df.loc[mask]


    
    
    return {
            'data': [{'x': filtered_df.fire_year.unique(),
                 'y': filtered_df.groupby('fire_year')['total_acres'].sum(),
                 'type':'bar'}
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'xaxis':{'title': 'Year'
                },
                'yaxis':{'title': 'Total Acres Burned'
                },
                'title': 'Total Acres Burned by Year due to {}'.format(cause)
            }
    }
       








# app callback for piechart by cause
@app.callback(
    Output('piechartYear', 'figure'),
    [Input('piechartInput', 'value')])
def update_piechart(year):
    piechart_df = df[df.fire_year == year]
    
    
    piechart = px.pie(
                    data_frame=piechart_df,
                    values='total_acres',
                    names='general_cause',
                    title='Oregon Wildfire Cause Distribution in {}'.format(year),
                    color_discrete_sequence=px.colors.cyclical.IceFire,
                    )
    
    piechart.update_traces(textposition='inside', textinfo='percent+label')
    
    return piechart










# app callback for pie chart by county
@app.callback(
    Output('piechartCounty', 'figure'),
    [Input('piechartCountyInput', 'value')])
def update_piechartCounty(year):
    piechart_df = df[df.fire_year == year]
    
    
    piechartCounty = px.pie(
                    data_frame=piechart_df,
                    values='total_acres',
                    names='county',
                    title='Oregon Wildfire County Distribution in {}'.format(year),
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    )
    
    piechartCounty.update_traces(textposition='inside', textinfo='percent+label')
    
    return piechartCounty
    






# app callback for pie chart by county
@app.callback(
    Output('piechartRedundant', 'figure'),
    [Input('piechartRedundantInput', 'value')])
def update_piechartCause(cause):
    piechart_df = df[df.general_cause == cause]
    
    
    piechartYear = px.pie(
                    data_frame=piechart_df,
                    values='total_acres',
                    names='fire_year',
                    title='Year Breakdown by {}'.format(cause),
                    color_discrete_sequence=px.colors.sequential.Magma,
                    )
    
    piechartYear.update_traces(textposition='inside', textinfo='percent+label')
    
    return piechartYear











if __name__ == '__main__':
    app.run_server(debug=True)













