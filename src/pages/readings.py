import dash_core_components as dcc
import dash.html as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests
import json
import os

from src import app

from dash.dependencies import Input, Output
from typing import List, Dict

endpoint_url = os.getenv('endpoint_url', '0.0.0.0')
endpoint_port = os.getenv('endpoint_port', 8010)

def get_data(device_name: str = "SolarMan") -> List[Dict]:
    url = f"http://{endpoint_url}:{endpoint_port}/api/v1.0/readings"
    payload = json.dumps({"device_name": device_name})
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, data=payload)
    return response.json()

def build_graph(data: List[Dict]) -> go.Figure:
    results = {
        'data': [
            go.Bar(
                x=[record['reading_timestamp'] for record in data],
                y=[record['reading_value'] for record in data],
            )
        ],
        'layout': go.Layout(
            title='Time Series Data',
            template='plotly_dark'
        )
    }
    return results

def build_table(data: List[Dict]) -> html.Table:
    results = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in ['Timestamp', 'Value']])
        ),
        html.Tbody([
            html.Tr([
                html.Td(record[col]) for col in ['reading_timestamp', 'reading_value']
            ]) for record in data
        ])
    ])
    return results

@app.callback(
    [Output('readings_chart', 'figure'),
     Output('data-table', 'children')],
    [Input('device-dropdown', 'value')]
)
def update_data(device_name: str):
    data = get_data(device_name)
    graph = build_graph(data)
    table = build_table(data)
    
    return graph, table

dropdown_layout = dbc.Row([
    dbc.Col(html.Fieldset([
        dbc.Label("Select Device"),
        dcc.Dropdown(
            id='device-dropdown',
            options=[
                {'label': 'SolarMan', 'value': 'SolarMan'},
                {'label': 'WaterTemperature', 'value': 'Aquarium-Temperature'},
                {'label': 'WaterManager', 'value': 'Aquarium-WaterManager-Develop'}
            ],
            value='SolarMan',
            className='custom-select'
        )
    ]), width=12)
])

layout = dbc.Container([
    dbc.Row([
        dbc.Col(width=2),
        dbc.Col([
            dropdown_layout,
            dcc.Graph(id='readings_chart'),
            html.Div(id='data-table')
        ], width=8),
        dbc.Col(width=2)
    ])
], fluid=True)
