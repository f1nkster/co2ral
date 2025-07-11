from typing import Any

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components.styles import text_elements as tx
from core.utils.images import get_base64_image
from dash import Input, Output, callback, html
from dash_iconify import DashIconify
from env import component_ids as comp_ids
from env import javascript_mapping as js


_ignored_pages = ["404"]

git_icon = get_base64_image("github.png")
dashboard_icon = get_base64_image("logo.png")

home_link = "/"
ui_link = "https://github.com/pfheiter/"


page_content: dict[str, dict[str, Any]] = {
    "home": {
        "name": "Home",
        "label": "Home",
        "icon": "fluent:water-32-filled",
    },
    "contact": {
        "name": "Contact",
        "label": "Contact",
        "icon": "fluent:water-32-filled",
    },
}


def get_navbar() -> dbc.Navbar:
    """Get the component to display the main navigation.

    :return: Main navigation Component which will be displayed by the browser.
    """
    # Title Elements
    logo = html.A(
        [
            DashIconify(icon="fluent:water-32-filled", width=32),
            DashIconify(icon="mdi:periodic-table-carbon-dioxide", width=32),
            DashIconify(icon="ic:baseline-model-training", width=32),
        ],
        href="/",
        className="dash-git-logo",
        style={"position": "relative", "left": "10px"},
    )

    title = html.Div(["CO", html.Sub(2), "RAL"])
    subtitle = html.A("A web UI for PyCO2", href=home_link, style=tx.subtitle)
    title_elements = dbc.Stack(
        [logo, dbc.NavbarBrand(dbc.Stack([title, subtitle]))],
        direction="horizontal",
        gap=4,
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

    dropdowns = dbc.Stack(nav_items, direction="horizontal", gap=3)

    panels = html.Div(
        id="navbar-dropdowns",
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        children=dropdowns,
        style={"width": "auto", "position": "absolute", "right": "160px"},
    )

    return dbc.Navbar(
        id="main-nav",
        children=[title_elements, panels, color_mode_switch, git_logo],
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


@callback(
    [
        [Output(i, "style") for i in list(dash.page_registry.values())],
    ],
    [
        Input("url", "search"),
        Input("url", "pathname"),
    ],
    disable_cache=True,
)
def update_nav_bar(search: str, pathname: str) -> tuple:
    """Update the navigation bar based on the url.

    :param search: Current url search, after the ?, e.g., ?par1=alkalinity.
    :param pathname: Current url pathname, after the slash /, e.g., /home.
    :return: List of navigation items to be displayed in the sub navigation.
    """
    path_list = pathname.split("/")
    default_dd_style = {"color": "white"}
    active_dd_style = {"color": "#19d83b", "font-weight": "bold", "transition": "all 0.3s ease"}
    nav_items = []
    # All sub-pages begin with /, so provide empty navigation, if we're on the landing page.
    if pathname != "/":
        # Ensure, that there is a path with a /
        if len(path_list) > 1:
            # set top level for streams or admin
            if len(path_list) > 3:
                root_level, top_level = path_list[1], path_list[2]
            else:
                root_level, top_level = path_list[0], path_list[1]
            top_name = page_content[root_level]["children"][top_level]["name"]
            top_icon = page_content[root_level]["children"][top_level]["icon"]
            nav_items.append(
                dbc.NavItem(
                    dmc.NavLink(
                        label=top_name,
                        leftSection=DashIconify(icon=top_icon, height=16),
                        rightSection=DashIconify(icon="tabler-chevron-right", height=16),
                        style={"height": "30px"},
                    ),
                )
            )
            for page in dash.page_registry.values():
                if (
                    top_level in page["relative_path"]
                    # and page["relative_path"].count("/") > 2
                    and ("hide" not in page or page["hide"] is False)
                ):
                    active = True if pathname == page["relative_path"] else False
                    style = (
                        {"height": "30px", "font-weight": "bold", "transition": "all 0.1s ease"}
                        if active
                        else {"height": "30px"}
                    )
                    if page["name"] in _ignored_pages:
                        continue
                    if page["name"] == "Documentation":
                        nav_items.append(
                            dbc.NavItem(
                                dmc.NavLink(
                                    label=page["name"],
                                    href=page["relative_path"],
                                    active=active,
                                    style=style,
                                ),
                                className="ms-auto",
                            )
                        )
                    else:
                        nav_items.append(
                            dbc.NavItem(
                                dmc.NavLink(
                                    label=f"{page['name']}",
                                    href=page["relative_path"] + search,
                                    style=style,
                                    active=active,
                                ),
                            )
                        )
    dd_active = [(i in path_list) for i in list(page_content.keys())]
    dd_styles = [active_dd_style if i else default_dd_style for i in dd_active]
    return (
        nav_items,
        dd_styles,
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
