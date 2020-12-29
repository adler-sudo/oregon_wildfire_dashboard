import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from firesByYear import app
import weather, fire, firesByYear


app.layout = html.Div([
    dcc.Link('go to weather', href='/weather'),
    html.Br(),
    dcc.Link('go to fire', href='/fire'),
    html.Br(),
    dcc.Link('go to fireByYear', href='/fireByYear'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/weather':
        return weather.layout
    elif pathname == '/fire':
        return fire.layout
    elif pathname == '/fireByYear':
        return firesByYear.layout

if __name__ == '__main__':
    app.run_server(debug=True)