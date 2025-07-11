import dash
import dash_bootstrap_components as dbc
from dash import html


dash.register_page(__name__, path="/contact")

layout = dbc.Container(
    [
        dbc.Row(html.H1("Contact: tba")),
    ]
)
