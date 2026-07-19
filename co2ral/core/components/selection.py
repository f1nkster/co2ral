from typing import Union

import dash_mantine_components as dmc
import numpy as np
from core.components.styles import text_elements as te
from dash import dcc, html
from dash.dependencies import Component
from dash_iconify import DashIconify
from env import colors as cols


EMPTY = html.Div("", className="mx-auto")


def dropdown_with_title(
    title: str,
    id: Union[dict, str],
    description: Union[None, str] = None,
    data: list = [],
    value: Union[None, list, str, int] = None,
    multi: bool = False,
    max_values: int = 5,
    persistence: bool = False,
    style: dict = {},
) -> Component:
    """Creates a dropdown with a title using the standard template

    :param title: Dropdown title
    :param id: id of the dropdown component
    :param description: text of the component
    :param data: Options that appear in the dropdown, defaults to None
    :param value: Values , defaults to None
    :param multi: if multiple options selection should be enabled, defaults to False
    :param max_values: max number of allowed values, defaults to 5
    :param persistence: to remember last state or not
    :param style: style of the dropdown component
    :return: Component
    """
    if multi:
        component = dmc.MultiSelect(
            label=title,
            description=description,
            data=data,
            value=value,
            id=id,
            maxValues=max_values,
            searchable=True,
            persistence=persistence,
            style=style,
        )
    else:
        component = dmc.Select(
            label=title,
            description=description,
            data=data,
            value=value,
            id=id,
            searchable=True,
            persistence=persistence,
            style=style,
        )
    return component


def accordion_with_title(
    title: str,
    content: html.Div,
    icon: str = "tabler:user",
    icon_color: str = "#007575",
    value: str = "Controls",
) -> html.Div:
    """Creates an accordion with several components

    :param title: title of accordion
    :param content: content elements
    :param icon: icon from dash iconify, defaults to "tabler:user"
    :param icon_color: color of the icon, defaults to "#007575"
    :param value: activated value, defaults to "Controls"
    :return: html.Div
    """
    accordion_items = dmc.AccordionItem(
        [
            dmc.AccordionControl(
                title,
                icon=DashIconify(
                    icon=icon,
                    color=icon_color,
                    width=30,
                ),
            ),
            dmc.AccordionPanel(content),
        ],
        value=title,
    )
    acc_container = html.Div(
        dmc.Accordion(
            multiple=True,
            children=accordion_items,
            value=value,
            radius=5,
            variant="filled",
            chevron=DashIconify(
                icon="line-md:chevron-triple-down",
                color=cols.DMC_THEME,
                width=32,
            ),
        ),
    )
    return acc_container


def range_slider(
    id: str,
    name: str,
    sub_text: Union[None, str] = None,
    value: list = [],
    min_val: Union[float, int] = 0,
    max_val: Union[float, int] = 100,
    unit: str = "",
    step: Union[float, int] = 1,
    labels_as_int: bool = True,
    info: Union[None, str] = None,
    disabled: bool = False,
) -> html.Div:
    """Creates a range slider

    :param id: id of element
    :param name: title of the element
    :param sub_text: short description if needed, defaults to None
    :param value: value selected , defaults to []
    :param min_val: min value on slider, defaults to 0
    :param max_val: max value on slider, defaults to 100
    :param unit: unit of measurement, defaults to ""
    :param step: step for slider, defaults to 1
    :param labels_as_int: labels as int or not, defaults to True
    :param info: explanation text shown in a tooltip next to the title, defaults to None
    :param disabled: greys out the slider, e.g. when its value is derived elsewhere
    :return: range slider element
    """
    # Create Marks
    num_marks: int = 5
    marks = np.linspace(min_val, max_val, num_marks)
    # Round the marks to an appropriate number of decimal places for readability
    if labels_as_int:
        rounded_marks = marks.astype(int)
    else:
        rounded_marks = np.round(marks, decimals=2)
    labelled_marks = [{"value": i, "label": f"{i}{unit}"} for i in rounded_marks]

    title = dmc.Text(name, style=te.component_text, id=f"{id}-title")
    title_row = info_disclosure(title, info) if info else title

    slider = html.Div(
        [
            title_row,
            dmc.Text(sub_text, size="xs", style=te.component_subtext),
            dmc.Slider(
                id=id,
                name=name,
                step=step,
                value=value,
                min=min_val,
                max=max_val,
                marks=labelled_marks,
                labelAlwaysOn=True,
                disabled=disabled,
                mt=28,
                # Update the value only when the user releases the handle, so live plot
                # updates trigger exactly one computation per adjustment.
                updatemode="mouseup",
            ),
        ]
    )

    return slider


def info_disclosure(title: Component, text: str) -> html.Details:
    """Wraps a title into a native details/summary element with an info icon:
       clicking the title or icon toggles the explanation text below.
       Native disclosure is used instead of a hover tooltip so it also works on touch devices.

    :param title: title component shown in the summary row
    :param text: explanation text shown when expanded
    :return: details element with title summary and explanation
    """
    return html.Details(
        [
            html.Summary(
                dmc.Group(
                    [title, DashIconify(icon="mdi:information-outline", width=16, color="#868e96")],
                    gap=6,
                ),
                className="info-summary",
            ),
            dmc.Text(text, size="xs", c="dimmed", mt=2, mb=4),
        ]
    )


def segmented_control(
    name: str,
    id: str | dict,
    data: dict = {},
    value: Union[None] = None,
    sub_text: Union[None, str] = None,
) -> html.Div:
    """Creates a segmented control with title

    :param name: title of the seg control
    :param id: id of component
    :param data: data dict, defaults to {}
    :param value: default value, defaults to None
    :param sub_text: subtext, defaults to None
    :return: segmented control container
    """
    data_list = [{"value": k, "label": v} for k, v in data.items()]
    segmented_control = html.Div(
        [
            dmc.Text(name, style=te.component_text),
            dmc.Text(sub_text, size="xs", style=te.component_subtext),
            dmc.SegmentedControl(
                id=id,
                value=value,
                persistence=True,
                data=data_list,
                mb=10,
                fullWidth=True,
            ),
        ]
    )
    return segmented_control


def badge(title: str) -> dmc.Badge:
    """Creates a badge used to highlight some parts within containers

    :param title: title of the badge
    :return: badge element
    """
    return dmc.Badge(
        title,
        variant="dot",
        radius="xs",
        size="md",
    )


def button(id: str, title: str, icon: str, color: str) -> dmc.Button:
    """Creates a button from mantine library with icon

    :param id: id of element
    :param title: title of element
    :param icon: icon name from iconify
    :param color: color of button
    :return: dmc.Button
    """
    return dmc.Button(
        title,
        id=id,
        variant="light",
        radius=0,
        fullWidth=True,
        leftSection=DashIconify(
            icon=icon,
            color=color,
            width=25,
        ),
        color=cols.DMC_GRAY,
    )


def wrap_spinner(component: html.Div) -> dcc.Loading:
    """Wraps a spinner around a component

    :param component: html component
    :return: dcc.Loading
    """
    return dcc.Loading(
        component,
        overlay_style={"visibility": "shown"},
        custom_spinner=DashIconify(
            icon="svg-spinners:blocks-shuffle-2",
            width=32,
            style={
                "position": "fixed",
                "top": "0",
                "left": "50%",
                "zIndex": "101",
                "marginTop": "10px",
                "min-width": "50px",
                "color": cols.LIGHT_GREEN,
            },
        ),
    )


def storage(id: str, spinner: bool = True) -> html.Div:
    """Creates a storage element

    :param id: id of element
    :param spinner: if it should be wrapped in storage
    :return: storage element
    """
    storage_base = html.Div(dcc.Store(id=id))
    if spinner:
        storage = wrap_spinner(storage_base)
    else:
        storage = storage_base

    return storage


def text_input(
    id: dict,
    title: str,
    value: str = "",
    description: str = "",
    placeholder: str = "",
    debounce: int = 2000,
    width: int = 150,
) -> dmc.TextInput:
    """Text input box, reads the input as a string

    :param id: pattern matching id
    :param title: title of element
    :param value: initial value
    :param description: description displayed under title, defaults to ""
    :param placeholder: description or placeholder in input box, defaults to ""
    :param debounce: time to wait before reading value unless enter is pushed (in ms), defaults to 500
    :param width: width of input box, defaults to 150
    :return: TextInput item
    """
    return dmc.TextInput(
        id=id,
        label=title,
        value=value,
        description=description,
        placeholder=placeholder,
        debounce=debounce,
        w=width,
    )


def get_common_legend(legend_names: list[str], label: bool = False) -> dmc.Card:
    """Creates a common legend element.

    :param legend_names: list of legends
    :param label: if label should also be shown in legend, defaults to False
    :return: dmc.Card of legend
    """
    legend_colors = cols.PLOT_COLORS
    if label:
        legend_names = ["Label"] + legend_names
        legend_colors = [cols.DMC_GRAY] + legend_colors
    legend_badge = [
        dmc.Badge(
            name,
            variant="light",
            leftSection=DashIconify(
                icon="akar-icons:square-fill",
                color=legend_colors[i],
                height=18,
            ),
            size="lg",
            radius="sm",
            fullWidth=True,
            color=legend_colors[i],
        )
        for i, name in enumerate(legend_names)
    ]

    legend = dmc.SimpleGrid(
        cols=len(legend_names),
        spacing="xs",
        verticalSpacing="xs",
        children=legend_badge,
    )

    legend_card = dmc.Card(
        legend,
        radius="md",
        withBorder=True,
        padding="xs",
    )

    return legend_card
