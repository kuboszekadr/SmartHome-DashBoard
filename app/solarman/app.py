import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from .pages import hour, day, home

layout = dbc.Col([
    dbc.Tabs([
        dbc.Tab(children=[home.layout], label='Home', tab_id='home'),
        dbc.Tab(children=[hour.layout], label='Hour', tab_id='hour'),
        dbc.Tab(children=[day.layout], label='Day', tab_id='day'),
    ],
        className='nav-fill',
        card=True,
        style={
            'margin-left': 'auto',
            'margin-right': 'auto', 
            'padding-bottom': '10px',
    })],
    style={
        'width': '95%',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'margin-top': '10px',
})


def init_app(server):
    app = dash.Dash(
        server=server,
        external_stylesheets=[dbc.themes.SLATE]
    )

    app.layout = layout

    hour.init_callbacks(app)
    day.init_callbacks(app)
    
    return app.server


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)

    with app.app_context():
        app = init_app(app)
    app.run()