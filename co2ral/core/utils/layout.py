from typing import Union

import dash
import dash_bootstrap_components as dbc
import dash_echarts
import dash_mantine_components as dmc
from dash import Input, Output, State, dcc, html
from dash.dependencies import Component
from dash_iconify import DashIconify
from env import colors
from env import javascript_mapping as js


def plot_cell(title: str, plot: Union[dash_echarts.DashECharts, dmc.Card]) -> html.Div:
    """Creates a plot cell for given title and plot.

    :param title: cell title
    :param plot: cell plot
    :return: html.Div containing cell title and plot
    """
    expand_id = f"{plot.id}_expand"
    modal_id = f"{plot.id}_cell"

    title_container = dmc.Badge(
        title,
        style={
            "border-bottom-left-radius": "0px",
            "border-bottom-right-radius": "0px",
            "display": "flex",
            "justify-content": "space-between",
            "align-items": "center",
            "padding-right": "0px",
        },
        fullWidth=True,
        variant="dot",
        radius="sm",
        size="lg",
        color=colors.DMC_GRAY,
        rightSection=dmc.ActionIcon(
            children=DashIconify(icon="map:fullscreen"),
            id=expand_id,
            color=colors.DMC_THEME,
            variant="subtle",
            size="lg",
        ),
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

    plot_container = dmc.Card(
        children=plot_with_spinner,
        style={
            "overflow": "visible",
            "border-top-left-radius": "0px",
            "border-top-right-radius": "0px",
        },
        radius="md",
        withBorder=True,
    )

    # Modal will be used to maximize the plot
    _modal = dmc.Modal(
        title=title,
        id=modal_id,
        size="60%",
        opened=False,
        radius="md",
        centered=True,
        lockScroll=True,
        transitionProps={"duration": 500, "transition": "pop"},
        styles={
            "title": {"font-size": "120%", "font-weight": "bold"},
            "header": {"background-color": colors.hex_to_rgba(colors.GRAY, 0.15)},
            "body": {"padding-top": "10px", "padding-bottom": "5px"},
            "close": {"color": colors.DMC_RED},
            "content": {"scale": "1.2"},
        },
    )

    cell_container = html.Div([_modal, title_container, plot_container], style={"width": "100%"})

    dash.clientside_callback(
        dash.ClientsideFunction(namespace=js.CLIENTSIDE, function_name=js.TOGGLE_MAP_FULLSCREEN),
        [
            Output(modal_id, "opened"),
        ],
        [
            Input(expand_id, "n_clicks"),
        ],
    )

    @dash.callback(
        [
            Output(modal_id, "children"),
            Output(plot.id, "children", allow_duplicate=True),
        ],
        [
            Input(modal_id, "opened"),
        ],
        [
            State(plot.id, "children"),
            State(modal_id, "children"),
        ],
        prevent_initial_call=True,
    )
    def toggle_modal_children(opened: int, plot_children: list, modal_children: list) -> tuple:
        """Toggles between plot children and modal children based on the opened state.

        :param opened: An integer indicating whether the modal is opened (non-zero) or closed (zero).
        :param plot_children: plot children to be displayed when the modal is closed.
        :param modal_children: modal children to be displayed when the modal is opened.
        :return: A tuple containing outputs
        """
        if opened:
            return (plot_children, None)
        else:
            return (None, modal_children)

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
                    dbc.Col(
                        control_layout,
                        width=3,
                    ),
                    dbc.Col(
                        output_layout,
                        width=9,
                    ),
                ],
            ),
        ],
    )

    panel_layout = html.Div([panel])
    return panel_layout
