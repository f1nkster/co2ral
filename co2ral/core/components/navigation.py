import urllib.parse

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components.styles import text_elements as tx
from core.utils.images import get_base64_image
from dash import Input, Output, callback, html
from dash_iconify import DashIconify
from env import component_ids as comp_ids
from env import javascript_mapping as js
from locales.translation import TRANSLATION_DICT


git_icon = get_base64_image("github.png")
dashboard_icon = get_base64_image("logo.png")

home_link = "/"
ui_link = "https://github.com/f1nkster/co2ral"

# The carbonate chemistry itself is computed by PyCO2SYS; the footer credits it.
PYCO2SYS_REPO = "https://github.com/mvdh7/PyCO2SYS"
PYCO2SYS_DOCS = "https://pyco2sys.readthedocs.io/"


def get_lang_from_search(search: str) -> str:
    """Reads the language from a url search string, falling back to German.

    :param search: Current url search, after the ?, e.g. "?lang=en".
    :return: Language code that exists in the translation dictionary.
    """
    query = search[1:] if search and search.startswith("?") else (search or "")
    lang = dict(urllib.parse.parse_qsl(query)).get("lang", "de")
    return lang if lang in TRANSLATION_DICT else "de"


def get_footer(lang: str = "de") -> html.Footer:
    """Get the page footer crediting PyCO2SYS, which performs all model calculations.

    :param lang: Language for the texts, either "de" or "en".
    :return: Footer component shown below the page content.
    """
    dictionary = TRANSLATION_DICT[lang]
    separator = dmc.Text("·", size="xs", c="dimmed")

    return html.Footer(
        dmc.Stack(
            [
                dmc.Text(dictionary["footer_credit"], size="xs", c="dimmed", ta="center"),
                dmc.Group(
                    [
                        dmc.Anchor(dictionary["footer_repo"], href=PYCO2SYS_REPO, target="_blank", size="xs"),
                        separator,
                        dmc.Anchor(dictionary["footer_docs"], href=PYCO2SYS_DOCS, target="_blank", size="xs"),
                        separator,
                        dmc.Anchor(dictionary["footer_source"], href=ui_link, target="_blank", size="xs"),
                    ],
                    gap="xs",
                    justify="center",
                ),
            ],
            gap=4,
        ),
        style={
            "borderTop": "1px solid var(--bs-border-color)",
            "marginTop": "32px",
            "padding": "16px 12px 24px",
        },
    )


@callback(
    Output("footer-container", "children"),
    Input("url", "search"),
)
def update_footer(search: str) -> html.Footer:
    """Update the footer when the language in the url changes.

    :param search: Current url search, after the ?, e.g. "?lang=de".
    :return: The footer component.
    """
    return get_footer(lang=get_lang_from_search(search))


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
    subtitle = html.A(
        TRANSLATION_DICT[lang]["app_subtitle"],
        href=home_link,
        style=tx.subtitle,
        id="subtitle-id",
        className="d-none d-md-block",
    )
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
        className="ms-auto d-none d-md-block",
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
        className="dash-git-logo d-none d-md-block",
        target="_blank",
        style={"position": "relative", "right": "5px"},
    )

    # Localized labels per page path; the registry name itself is language independent.
    page_labels = {
        "/": TRANSLATION_DICT[lang]["nav_home"],
        "/ozean": TRANSLATION_DICT[lang]["nav_ocean"],
        "/lehrkraefte": TRANSLATION_DICT[lang]["nav_teachers"],
    }

    style = {"height": "30px", "color": "white"}
    nav_items = []
    for page in dash.page_registry.values():
        path = page["relative_path"]
        nav_items.append(
            dbc.NavItem(
                dmc.NavLink(
                    label=page_labels.get(path, page["name"]),
                    # Keep the language when navigating between pages.
                    href=f"{path}?lang={lang}",
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
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 d-none d-lg-block",
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
