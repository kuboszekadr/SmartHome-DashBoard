import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash

from dash.dependencies import Input, Output
from components import single_date_picker, next_btn, prev_btn, card

data = None
data_chart = dcc.Graph(id='day-chart')

total_period_card = card('total-period', '00.00 kWh', 'Period total generation')
max_period_card = card('max-period', '00.00 kWh @ 1900-01-01', 'Period max')
avg_period_card = card('avg-period', '00.00 kWh', 'Period avg')

layout = dbc.Col([
    dbc.Row([
        dbc.Col(total_period_card),
        dbc.Col(max_period_card),
        dbc.Col(avg_period_card),
    ]),
    data_chart,
    dbc.Col([
        dbc.Row([
            prev_btn('day-prev-btn'),
            single_date_picker('day-date-picker'),
            next_btn('day-next-btn'),
        ])], 
    )
])


def load_data():
    data = pd.read_csv(
        r'C:\GIT\Private\SmartHome-FrontEnd\data\2021_05_28.csv', skip_blank_lines=True)
    data['reading_timestamp'] = pd.to_datetime(data['reading_timestamp'])

    data.sort_values(by='reading_timestamp', inplace=True)
    data.reindex()

    data_by_device = data.groupby(by=['device_id'])
    solar = data_by_device.get_group(3).copy()
    solar['reading_date'] = solar['reading_timestamp'].apply(
        lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))

    solar_by_date = solar.groupby(by=['reading_date'])

    return solar_by_date


def init(server):
    app = dash.Dash(
        __name__,
        server=server,
        external_stylesheets=[dbc.themes.SLATE]
    )

    app.layout = layout
    init_callbacks(app)

    return app.server


def init_callbacks(app):
    data = load_data()

    @app.callback(
        Output(component_id='day-chart', component_property='figure'),
        Input(component_id='day-date-picker', component_property='date')
    )
    def show_daily_graph(date):
        daily_data = data['reading_value'].sum()

        fig = px.bar(
            x=daily_data.index,
            y=daily_data.values / 100.0,
            template='plotly_dark',
            title='Daily power generation'
        )

        fig.update_layout(
            title={'x': 0.5},
            xaxis={'title_text': 'Day'},
            yaxis={
                'title_text': 'Power generation [kWh]',
                'rangemode': 'nonnegative'
            },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )

        return fig


if __name__ == '__main__':

    from flask import Flask
    app = Flask(__name__)

    with app.app_context():
        app = init(app)
    app.run()
