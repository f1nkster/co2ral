import pathlib
import urllib.parse

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components.styles import text_elements as tx
from core.utils.images import get_base64_image
from dash import Input, Output, State, callback, html
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

# University logos are not part of the repository (see .gitignore) and have to be placed
# in the assets folder on each machine. Any file extension works.
#
# Two variants, named after the theme they are shown in: the header is white in light mode
# and dark in dark mode, so each needs a logo with the opposite ink.
ASSETS_DIR = pathlib.Path(__file__).resolve().parents[2] / "assets"
PARTNER_LOGO_STEMS = {
    "light": ("fau-logo-light",),
    "dark": ("fau-logo", "LogoChemiedidaktik"),
}


def get_partner_logo_src(theme: str = "dark") -> str | None:
    """Finds the university logo for one theme in the assets folder.

    Resolved per call, so a logo appears as soon as the file is dropped in, without
    restarting the app.

    :param theme: "light" for the dark-ink logo, "dark" for the light-ink one.
    :return: Asset url of the logo, or None if no matching file is present.
    """
    for stem in PARTNER_LOGO_STEMS.get(theme, ()):
        for candidate in sorted(ASSETS_DIR.glob(f"{stem}.*")):
            return f"/assets/{candidate.name}"
    return None


def _logo_image(source: str, class_name: str = "") -> html.Img:
    """Builds the logo image shown in the header.

    :param source: Asset url of the logo file.
    :param class_name: Extra class used to switch variants per theme.
    :return: Image component.
    """
    return html.Img(
        src=source,
        alt="FAU Erlangen-Nürnberg",
        height="34px",
        className=class_name,
        style={"marginRight": "12px"},
    )


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


def _nav_links(lang: str, page_labels: dict[str, str]) -> list:
    """Builds the page links of the header, including the imprint.

    One list serves both layouts: bootstrap lays them out in a row from the lg breakpoint
    up and stacks them behind the toggler below it.

    :param lang: Selected language.
    :param page_labels: Localized label per page path.
    :return: List of nav links.
    """
    links = [
        dbc.NavLink(
            page_labels.get(page["relative_path"], page["name"]),
            # Keep the language when navigating between pages.
            href=f"{page['relative_path']}?lang={lang}",
        )
        for page in dash.page_registry.values()
    ]
    links.append(
        dbc.NavLink(
            TRANSLATION_DICT[lang]["imprint"],
            href="https://www.chemiedidaktik.phil.fau.de/impressum/",
            external_link=True,
        )
    )
    return links


@callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_mobile_navigation(n_clicks: int, is_open: bool) -> bool:
    """Opens and closes the stacked navigation on small screens.

    :param n_clicks: Number of clicks on the toggler.
    :param is_open: Whether the navigation is currently open.
    :return: The new open state.
    """
    return not is_open


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

    # University logo, resolved from the assets folder. Both variants are rendered and the
    # stylesheet shows the one matching the theme; when only one file exists it is used for
    # both, and with none at all the logo is omitted rather than shown broken.
    light_logo = get_partner_logo_src("light") or get_partner_logo_src("dark")
    dark_logo = get_partner_logo_src("dark") or get_partner_logo_src("light")

    if not light_logo:
        logo_images = []
    elif light_logo == dark_logo:
        logo_images = [_logo_image(light_logo)]
    else:
        logo_images = [
            _logo_image(light_logo, "fau-logo-for-light"),
            _logo_image(dark_logo, "fau-logo-for-dark"),
        ]

    logo_cd = (
        html.A(
            logo_images,
            href="https://www.chemiedidaktik.phil.fau.de/",
            style={"width": "auto"},
            className="d-none d-md-block",
        )
        if logo_images
        else None
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
        className="g-0 flex-nowrap mt-3 mt-md-0",
        style={"width": "auto", "marginRight": "12px"},
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

    # A single set of links inside the collapse: bootstrap's navbar-expand-lg shows them in
    # a row from lg up and hides them behind the toggler below it. The links used to be a
    # separate row hidden with d-none, which left the other pages unreachable on a phone.
    toggler = dbc.NavbarToggler(id="navbar-toggler", n_clicks=0, className="d-lg-none")
    navigation_links = dbc.Collapse(
        dbc.Nav(_nav_links(lang, page_labels), id="navbar-dropdowns", navbar=True, className="ms-auto"),
        id="navbar-collapse",
        is_open=False,
        navbar=True,
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
        children=[
            child
            for child in [
                title_elements,
                toggler,
                navigation_links,
                logo_cd,
                color_mode_switch,
                lang_switch,
                git_logo,
            ]
            if child is not None
        ],
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
