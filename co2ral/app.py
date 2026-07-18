import datetime

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import env.colors as colors
from dash import Dash, dcc, html


dash._dash_renderer._set_react_version("18.2.0")

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.FONT_AWESOME,
        dmc.styles.CAROUSEL,
        dmc.styles.CHARTS,
        "/assets/custom.css",
    ],
    use_pages=True,
)

app.title = "co2ral"
app.config["suppress_callback_exceptions"] = True

# Set main layout.
app.layout = dmc.MantineProvider(
    id="dmc-main",
    theme={"primaryColor": colors.DMC_THEME},
    children=[
        # navigation.get_navbar(),
        html.Div(id="navbar-container"),
        dcc.Location(id="url", refresh=False),
        html.Div(
            id="main-container",
            children=[dash.page_container],  # page_container automatically contains the content based on the url.
        ),
    ],
)

# Print time of load. Useful when running with use_reloader=True.
print(f"Reload WebApp at: {datetime.datetime.now()}")
