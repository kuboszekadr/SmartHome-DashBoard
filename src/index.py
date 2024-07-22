import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from src import app
from src.pages import devices, readings
from src.pages.navbar import navbar

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/devices' or pathname == '/':
        return devices.layout
    elif pathname == '/readings':
        return readings.layout
    else:
        return '404'