import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from firesByYear import app
import weather, fire, firesByYear, radius_fire, radius_weather, choropleth_experimental


app.layout = html.Div([
    html.Div(id='header-div',
             children=[
                 html.H1('Oregon Wildfire Dashboard'),
                 html.H6('An AI application for Oregon wildfire prediction and prevention')
                 ]
             ),
    dcc.Tabs(id='tabs',
             value='tab-6',
             children=[
                 dcc.Tab(label='fireByYear', value='tab-1'),
                 dcc.Tab(label='fire', value='tab-2'),
                 dcc.Tab(label='fire-radius', value='tab-3'),
                 dcc.Tab(label='weather', value='tab-4'),
                 dcc.Tab(label='weather-radius', value='tab-5'),
                 dcc.Tab(label='choropleth-all', value='tab-6')
             ]),
    html.Div(id='tab-driven-page-content')
])

@app.callback(Output('tab-driven-page-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return firesByYear.layout
    if tab == 'tab-2':
        return fire.layout
    if tab == 'tab-3':
        return radius_fire.layout
    if tab == 'tab-4':
        return weather.layout
    if tab == 'tab-5':
        return radius_weather.layout
    if tab == 'tab-6':
        return choropleth_experimental.layout

if __name__ == '__main__':
    app.run_server(debug=True)