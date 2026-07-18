import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components.styles import text_elements as tx
from core.utils.images import get_base64_image
from dash import Input, Output, html
from dash_iconify import DashIconify
from env import component_ids as comp_ids
from env import javascript_mapping as js
from locales.translation import TRANSLATION_DICT


git_icon = get_base64_image("github.png")
dashboard_icon = get_base64_image("logo.png")

home_link = "/"
ui_link = "https://github.com/f1nkster/co2ral"


def get_navbar(lang: str = "de") -> dbc.Navbar:
    """Get the component to display the main navigation.

    :param lang: Language for the subtitle, either "de" or "en".
    :return: Main navigation Component which will be displayed by the browser.
    """
    # Title Elements
    logo = html.A(
        [
            DashIconify(icon="game-icons:coral", width=32),
        ],
        href="/",
        style={"position": "relative", "left": "10px"},
    )

    title = html.Div(["CO", html.Sub(2), "RAL"])
    subtitle = html.A(TRANSLATION_DICT[lang]["app_subtitle"], href=home_link, style=tx.subtitle, id="subtitle-id")
    title_elements = dbc.Stack(
        [logo, dbc.NavbarBrand(dbc.Stack([title, subtitle]))],
        direction="horizontal",
        gap=4,
    )

    # Logo from assets
    logo_cd = html.A(
        [
            html.Img(
                src="/assets/LogoChemiedidaktik.svg",
                height="40px",
                style={"marginRight": "12px"},
            )
        ],
        href="https://www.chemiedidaktik.phil.fau.de/",
        style={"width": "auto", "right": "23px"},
        className="ms-auto",
    )

    # Theme Switching
    color_mode_switch = html.Div(
        [
            dmc.Switch(
                thumbIcon=DashIconify(icon="line-md:cog-filled-loop", color="green"),
                offLabel=DashIconify(icon="meteocons:falling-stars", width=22),
                onLabel=DashIconify(icon="meteocons:clear-day-fill", width=22),
                size="sm",
                id=comp_ids.THEME_SWITCH,
                checked=True,
                persistence=True,
                color="rgba(39, 174, 96 , 0.2)",
            ),
        ],
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        style={"width": "auto", "position": "relative", "right": "23px"},
    )

    # Git Logo
    git_logo = html.A(
        [html.Img(src=f"data:image/png;base64,{git_icon}", height="32px")],
        href=ui_link,
        className="dash-git-logo",
        target="_blank",
        style={"position": "relative", "right": "5px"},
    )

    nav_items = []
    for page in dash.page_registry.values():
        style = {"height": "30px", "color": "white"}
        nav_items.append(
            dbc.NavItem(
                dmc.NavLink(
                    label=f"{page['name']}",
                    href=page["relative_path"],
                    style=style,
                ),
            )
        )

    # add legal notice
    nav_items.append(
        dbc.NavItem(
            dmc.NavLink(
                label=TRANSLATION_DICT[lang]["imprint"],
                href="https://www.chemiedidaktik.phil.fau.de/impressum/",
                style=style,
            ),
        )
    )
    dropdowns = dbc.Stack(nav_items, direction="horizontal", gap=3)

    panels = html.Div(
        id="navbar-dropdowns",
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        children=dropdowns,
        style={"width": "auto", "position": "absolute", "right": "240px"},
    )

    lang_switch = dmc.SegmentedControl(
        id="lang-segmented",
        data=[
            {"label": "🇬🇧 EN", "value": "en"},
            {"label": "🇩🇪 DE", "value": "de"},
        ],
        value=lang,
        size="sm",
        style={
            "width": 120,
            "marginRight": "16px",
            "background": "#222",  # or your preferred color
            "color": "#fff",  # text color
            "border": "1px solid #444",  # border color
        },
    )

    return dbc.Navbar(
        id="main-nav",
        children=[title_elements, panels, logo_cd, color_mode_switch, lang_switch, git_logo],
        dark=True,
        color="#141B21",
        sticky="top",
        style={
            "width": "auto",
            "align-content": "center",
            "height": "50px",
            "zIndex": "100",
        },
    )


# Bootstrap Theme switch callback
dash.clientside_callback(
    dash.ClientsideFunction(namespace=js.CLIENTSIDE, function_name=js.SET_BOOTSTRAP_THEME),
    Output(comp_ids.THEME_SWITCH, "children"),
    Input(comp_ids.THEME_SWITCH, "checked"),
)

# Mantine Theme switch callback
dash.clientside_callback(
    dash.ClientsideFunction(namespace=js.CLIENTSIDE, function_name=js.SET_MANTINE_THEME),
    Output("dmc-main", "forceColorScheme"),
    Input(comp_ids.THEME_SWITCH, "checked"),
)
