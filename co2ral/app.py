import datetime

import dash
import dash_mantine_components as dmc
import env.colors as colors
from dash import Dash, dcc, html


dash._dash_renderer._set_react_version("18.2.0")

# All stylesheets are served locally from the assets folder (GDPR: no CDN or Google Fonts
# requests): the Bootstrap Flatly theme and the self-hosted Lato font live in assets/,
# which dash includes automatically. Mantine styles ship bundled with the component library.
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
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
        html.Div(id="footer-container"),
    ],
)

# Print time of load. Useful when running with use_reloader=True.
print(f"Reload WebApp at: {datetime.datetime.now()}")
