import dash_bootstrap_components as dbc
import dash_core_components as dcc
import datetime
import pandas as pd
import plotly.express as px
import dash

from dash.dependencies import Input, Output
from components import single_date_picker, next_btn, prev_btn, card

data = None
data_chart = dcc.Graph(id='hour-chart')

total_daily_card = card('total-daily', '00.00 kWh', 'Daily generation')
max_daily_card = card('max-daily', '00.00 kWh @ 12:00', 'Day max')
runtime_card = card('runtime', '10h 53m', 'Active')

layout = dbc.Col([
    dbc.Row([
        dbc.Col(total_daily_card),
        dbc.Col(max_daily_card),
        dbc.Col(runtime_card)
    ]),
    data_chart,
    dbc.Col([
        dbc.Row([
            prev_btn('hour-prev-btn'),
            single_date_picker('hour-date-picker'),
            next_btn('hour-next-btn'),
        ])
    ])
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
        Output(component_id='hour-chart', component_property='figure'),
        Output(component_id='total-daily', component_property='children'),
        Output(component_id='max-daily', component_property='children'),
        Input(component_id='hour-date-picker', component_property='date')
    )
    def get_hour_chart(date):
        solar_data = data.get_group(
            date + ' 00:00:00').copy().drop_duplicates()
        solar_data['values2'] = solar_data['reading_value'].diff()

        fig = px.line(
            x=solar_data['reading_timestamp'],
            y=solar_data['values2'],
            color=solar_data['measure_id'].astype(str),
            template='plotly_dark',
            title='Daily power generation')

        fig.update_layout(
            title={'x': 0.5},
            xaxis={'title_text': 'Hour'},
            yaxis={
                'title_text': 'Power generation [kWh]',
                'rangemode': 'nonnegative'
            },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )

        daily_generation = round(solar_data['values2'].sum(), 2)

        max_id = solar_data['values2'].idxmax()

        daily_max, daily_timestamp = solar_data.loc[max_id, ['values2', 'reading_timestamp']]
        daily_timestamp = daily_timestamp.strftime('%H:%M')

        return [
            fig, 
            f'{daily_generation:.2f} kWh',
            f'{daily_max:.2f} kWh @ {daily_timestamp}'
            ]

    @app.callback(
        Output(component_id='hour-date-picker', component_property='date'),
        Input(component_id='hour-date-picker', component_property='date'),
        Input(component_id='hour-prev-btn', component_property='n_clicks'),
        Input(component_id='hour-next-btn', component_property='n_clicks'),
    )
    def change_date(date, *args):
        ctx = dash.callback_context

        if not ctx.triggered:
            return date
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        increment = -1 if button_id == 'hour-prev-btn' else 1
        new_date = datetime.datetime.strptime(
            date, '%Y-%m-%d') + datetime.timedelta(days=increment)

        return new_date.date()


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)

    with app.app_context():
        app = init(app)
    app.run(debug=True)
