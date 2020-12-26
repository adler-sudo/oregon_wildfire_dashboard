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

# select geo table
geo = Table('geo', metadata, autoload=True, autoload_with=engine)
queryGeo = select([geo])
recordsGeo = conn.execute(queryGeo).fetchall()
dfGeo = pd.DataFrame(recordsGeo, columns=geo.columns.keys())
dfGeo.drop(columns=['index'], inplace=True)
dfGeo.dropna(subset=['total_acres'], inplace=True)

# initiate app
app = dash.Dash(__name__)


fig = px.scatter(dfGeo, x='longitude', y='latitude', color='total_acres')


app.layout = html.Div(
    children=[
        dcc.Graph(
            figure=fig
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
