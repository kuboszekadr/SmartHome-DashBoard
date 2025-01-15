import dash_core_components as dcc
import dash.html as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests
import json
import os

from src import app
from dash.dependencies import Input, Output, State
from dash import callback_context

from typing import List, Dict
from datetime import datetime, timedelta

endpoint_url = os.getenv('endpoint_url', '0.0.0.0')
endpoint_port = os.getenv('endpoint_port', 8010)

def get_data(device_name: str = "tauron-emeter", date: str = None) -> List[Dict]:
    url = f"http://{endpoint_url}:{endpoint_port}/api/v1.1/readings"
    
    payload = {"device_name": device_name}
    if date:
        payload["date"] = date
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, data=json.dumps(payload))

    return response.json()

def build_graph(data: List[Dict]) -> go.Figure:
    oze_data = [record for record in data if record['measure_name'] == 'oze']
    consume_data = [record for record in data if record['measure_name'] == 'consum']

    results = {
        'data': [
            go.Bar(
                x=[record['reading_timestamp'] for record in oze_data],
                y=[record['reading_value'] for record in oze_data],
                name='OZE'
            ),
            go.Bar(
                x=[record['reading_timestamp'] for record in consume_data],
                y=[record['reading_value'] for record in consume_data],
                name='CONSUME'
            )
        ],
        'layout': go.Layout(
            title='Tauron Data',
            template='plotly_dark',
            barmode='group'
        )
    }
    return go.Figure(results)

@app.callback(
    [Output('tauron-chart', 'figure'),
     Output('oze-sum', 'children'),
     Output('consum-sum', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('date-picker', 'date')]
)
def update_on_interval(_, selected_date):
    data = get_data(date=selected_date)
    figure = build_graph(data)
    
    oze_sum = sum(record['reading_value'] for record in data if record['measure_name'] == 'oze')
    consum_sum = sum(record['reading_value'] for record in data if record['measure_name'] == 'consum')
    
    return [
        figure, 
        round(oze_sum, 2), 
        round(consum_sum, 2)
    ]

@app.callback(
    [Output('date-picker', 'date')],
    [Input('prev-date-button', 'n_clicks'),
     Input('next-date-button', 'n_clicks')],
    [State('date-picker', 'date')]
)
def update_date(prev_clicks, next_clicks, current_date):
    if not current_date:
        current_date = datetime.now().date()
    else:
        current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
    
    ctx = callback_context

    if not ctx.triggered:
        return [current_date]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'prev-date-button':
            new_date = current_date - timedelta(days=1)
        elif button_id == 'next-date-button':
            new_date = current_date + timedelta(days=1)
        else:
            new_date = current_date

    return [new_date]

layout = dbc.Container([
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # 30 seconds
        n_intervals=0
    ),
    dbc.Row([
        dbc.Col(width=2),
        dbc.Col([
            dcc.DatePickerSingle(
                id='date-picker',
                date=datetime.now().date(),
                display_format='YYYY-MM-DD'
            ),
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        "<", 
                        id='prev-date-button', 
                        color='primary', 
                        className='mr-2',
                        style={'height': '100%'}
                    ),
                    width='auto',
                    style={'display': 'flex', 'align-items': 'center'}
                ),
                dbc.Col(
                    dcc.Graph(id='tauron-chart'),
                    width=True
                ),
                dbc.Col(
                    dbc.Button(
                        ">",
                        id='next-date-button', 
                        color='primary', 
                        className='ml-2',
                        style={'height': '100%'}
                    ),
                    width='auto',
                    style={'display': 'flex', 'align-items': 'center'}
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("OZE [kWh]", className="card-title"),
                            html.P(id='oze-sum', className="card-text"),
                        ]),
                        className="mb-3"
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("CONSUM [kWh]", className="card-title"),
                            html.P(id='consum-sum', className="card-text"),
                        ]),
                        className="mb-3"
                    )
                )
            ])
        ], width=8),
        dbc.Col(width=2)
    ])
], fluid=True)