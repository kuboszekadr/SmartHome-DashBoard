import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime, timedelta

from src import app

# Mock time series data
data = [{'Date': (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d'), 'Value': v} for i, v in enumerate(range(10, 20))]

chart_layout = dcc.Graph(
                id='time-series-chart',
                figure={
                    'data': [
                        go.Bar(
                            x=[record['Date'] for record in data],
                            y=[record['Value'] for record in data],
                        )
                    ],
                    'layout': go.Layout(
                        title='Time Series Data',
                        template='plotly_dark'
                    )
                }
            )

table_layout = html.Table([
    html.Thead(
        html.Tr([html.Th(col) for col in ['Date', 'Value']])
    ),
    html.Tbody([
        html.Tr([
            html.Td(record[col]) for col in ['Date', 'Value']
        ]) for record in data
    ])
])

# Devices page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div(), width=2),
        dbc.Col([chart_layout, table_layout], width=8),
        dbc.Col(html.Div(),width=2)
    ])
], fluid=True)