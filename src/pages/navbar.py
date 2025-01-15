import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Devices", href="/devices")),
        dbc.NavItem(dbc.NavLink("Readings", href="/readings")),
        dbc.NavItem(dbc.NavLink("Tauron", href="/tauron")),
    ],
    brand="SmartHome",
    brand_href="#",
    color="primary",
    dark=True,
    style={'marginBottom': 20}  # Add margin bottom
)