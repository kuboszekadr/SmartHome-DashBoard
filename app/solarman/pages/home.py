import dash
import dash_daq as daq
import dash_bootstrap_components as dbc

import dash_html_components as html

from components import card

current_power = card(
    'current-power',
    '4.5kWh',
    'Current power'
)

avg_comparison = card(
    'avg',
    '+5%',
    'From average'
)


today_generation = card(
    'today-generation',
    '4.5kWh',
    'Today generation'
)


up_time = card(
    'uptime',
    '5:28h',
    'Uptime'
)

start_time = card(
    'start-time',
    '3:45',
    'System start'
)


layout = dbc.Col([
    dbc.Row([
        current_power,
        dbc.Col([
            dbc.Row([
                dbc.Col(today_generation),
                dbc.Col(avg_comparison),
            ]),
            dbc.Row([
                dbc.Col(start_time),
                dbc.Col(up_time),
            ])
        ])
    ]),
    html.Div([
        "Last update: 15:30"], style={
        'text-align': 'center',
        'width': '100%',
        'position': 'fixed',
        'bottom': 10,
    })
])


def init(server):
    app = dash.Dash(
        __name__,
        server=server,
        external_stylesheets=[dbc.themes.SLATE]
    )

    app.layout = layout
    return app.server


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)

    with app.app_context():
        app = init(app)
    app.run(debug=True)
