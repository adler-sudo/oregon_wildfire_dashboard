# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:17:11 2020

@author: james
"""

# exploratory data analysis on weather data
import sqlalchemy
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def weatherEDA(location, parameter):
    """analyze a weather parameter of a location overtime
    
    location: location of interest (one name may encompass many locations)
    
    parameter: parameter of interest (TAVG, TMAX, TMIN, PRCP, SNOW)
    """
    
    # connect to the engine
    engine = sqlalchemy.create_engine('sqlite:///weatherData.db')
    conn = engine.connect()
    
    # query the desired data
    query = "SELECT NAME, DATE, {} FROM observations".format(parameter)
    results = conn.execute(query).fetchall()
    
    # organize into dataframe
    df = pd.DataFrame(results, columns=['NAME', 'DATE', parameter])
    df.sort_values('DATE', inplace=True)
    
    # define all locations of interest
    locations = [i for i in df.NAME if location in i]
    locations = list(set(locations))
    
    # create and show figure
    fig = px.line()
    
    for i in locations:
        di = df[df.NAME == i]
        fig.add_trace(go.Scatter(x=di.DATE,
                                 y=di[parameter],
                                 line=go.scatter.Line(color='blue')))

    fig.update_layout(dict(title='{} in {} from 1960-2020'.format(location, parameter)))
    
    return fig