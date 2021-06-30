import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from datetime import date


def prev_btn(element_id: str):
    btn = dbc.Button(
        children=['❮ Previous'],
        style={
            'position': 'absolute',
            'left': '0',
            'width': '10%'
        },
        id=element_id,
    )

    return btn


def next_btn(element_id: str):
    btn = dbc.Button(
        children=['Next ❯'],
        style={
            'position': 'absolute',
            'right': '0',
            'width': '10%'},
        id=element_id
    )

    return btn


def single_date_picker(element_id: str):
    date_picker = dcc.DatePickerSingle(
        id=element_id,
        min_date_allowed=date(2021, 1, 1),
        max_date_allowed=date(2021, 12, 31),
        initial_visible_month=date(2021, 12, 31),
        date=date(2021, 5, 25),
        first_day_of_week=1,
        display_format='DD-MM-YYYY',
        style={
            'position': 'absolute',
            'left': '50%',
            'right': '50%',
            'text-align': 'center'
        }
    )

    return date_picker

def card(element_id: str, text: str, description: str):
    content = html.P(text, className='card-text', id=element_id)
    footer_content = html.Small(description, className='text-muted')

    card_body = dbc.CardBody([content, footer_content])
    _card = dbc.Card(card_body)

    return _card