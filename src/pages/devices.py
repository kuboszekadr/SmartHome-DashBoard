import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import os
import requests

from dash import dash_table
from dash.dependencies import Input, Output

from src import app 

endpoint_url = os.getenv('endpoint_url', '0.0.0.0')
endpoint_port = os.getenv('endpoint_port', 8010)

columns = [
    {'name': 'Device ID', 'id': 'device_id'},
    {'name': 'Device IP', 'id': 'device_ip'},
    {'name': 'Device Name', 'id': 'device_name'},
    {'name': 'Last Updated', 'id': 'last_update'}
]

table_layout = dash_table.DataTable(
    id='table',
    columns=columns,
    sort_action='native',
    style_as_list_view=True,
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    }
)

interval_layout = dcc.Interval(
    id='interval-component',
    interval=60*1000, # in milliseconds
    n_intervals=0
)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div(), width=2),
        dbc.Col(table_layout, width=8),
        dbc.Col(html.Div(), width=2)
    ]),
    interval_layout
], fluid=True)


@app.callback(
    Output('table', 'data'),
    [Input('interval-component', 'n_intervals')]
)
def update_table(n):
    data = requests.get(f'http://{endpoint_url}:{endpoint_port}/api/v1.0/devices').json()
    return data