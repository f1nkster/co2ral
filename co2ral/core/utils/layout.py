from typing import Union

import dash_bootstrap_components as dbc
import dash_echarts
import dash_mantine_components as dmc
from dash import dcc, html
from dash.dependencies import Component
from dash_iconify import DashIconify
from env import colors


def plot_cell(
    title: str,
    plot: Union[dash_echarts.DashECharts, dmc.Card],
    style: dict = {"width": "100%", "margin-bottom": "20px"},
    subtitle: Union[None, str, list] = None,
    with_download: bool = True,
) -> html.Div:
    """Creates a plot cell for given title and plot.

    :param title: cell title
    :param plot: cell plot
    :param style: style for the overall cell container
    :param subtitle: context line(s) with the fixed model conditions, shown above the plot
    :param with_download: whether to render the PNG download button in the title bar
    :return: html.Div containing cell title and plot
    """
    download_button = (
        html.Button(
            dmc.ActionIcon(
                children=DashIconify(icon="lucide:download"),
                color=colors.DMC_THEME,
                variant="subtle",
                size="lg",
            ),
            id={"type": "download-btn", "index": plot.id},
            n_clicks=0,
            style={"background": "none", "border": "none", "padding": 0, "cursor": "pointer"},
        )
        if with_download
        else None
    )

    title_container = dmc.Badge(
        title,
        className="plot-title-badge",
        style={
            "border-bottom-left-radius": "0px",
            "border-bottom-right-radius": "0px",
            "display": "flex",
            "justify-content": "space-between",
            "align-items": "center",
            "padding-right": "0px",
            "textTransform": "none",
        },
        fullWidth=True,
        variant="dot",
        radius="sm",
        size="lg",
        color=colors.DMC_GRAY,
        rightSection=download_button,
    )

    plot_with_spinner = dcc.Loading(
        plot,
        overlay_style={"visibility": "shown"},
        custom_spinner=DashIconify(
            icon="eos-icons:hourglass",
            width=27,
            style={
                "position": "absolute",
                "color": colors.THEME,
                "top": "0",
                "right": "0%",
                "zIndex": "99",
            },
        ),
    )

    card_children = []
    if subtitle:
        subtitle_lines = subtitle if isinstance(subtitle, list) else [subtitle]
        for line in subtitle_lines:
            card_children.append(dmc.Text(line, size="xs", c="dimmed", mb=6))
    card_children.append(plot_with_spinner)

    plot_container = dmc.Card(
        children=card_children,
        style={
            "overflow": "visible",
            "border-top-left-radius": "0px",
            "border-top-right-radius": "0px",
        },
        radius="md",
        withBorder=True,
    )

    # Full width and height, so cells sharing a grid row line up and stretch equally.
    cell_style = {**style, "width": "100%", "display": "flex", "flexDirection": "column"}
    cell_container = html.Div([title_container, plot_container], style=cell_style)

    return cell_container


def get_generic_layout(
    control_layout: Component,
    output_layout: Component,
) -> Component:
    """Will construct the overall layout of the page.
    :param control_layout: Control layout (buttons and dropdowns)
    :param output_layout: Output layout containing plots and tables
    :returns:  the layout
    """
    panel = dbc.Col(
        [
            dbc.Row(None, style={"height": "10px"}),
            dbc.Row(
                [
                    # Side by side on large screens, stacked (controls on top) on tablets and phones.
                    dbc.Col(
                        control_layout,
                        xs=12,
                        lg=3,
                    ),
                    dbc.Col(
                        output_layout,
                        xs=12,
                        lg=9,
                    ),
                ],
            ),
        ],
    )

    panel_layout = html.Div([panel])
    return panel_layout
