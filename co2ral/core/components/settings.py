import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components import selection as sel
from core.utils.marine_model import (
    DIC_PARAMS,
    SYSTEM_PARAMS,
)
from dash import html
from env.colors import DMC_LIME, DMC_RED


def create_basic_settings() -> dmc.Accordion:
    """Create the basic settings accordion for the marine model.

    :return: The basic settings accordion component.
    """
    content = []

    fixed_param_data = SYSTEM_PARAMS.get_option_list()
    content.append(
        sel.dropdown_with_title(
            "Fixed Parameter",
            id="par1-dd",
            description="Parameter which is fixed to a single value for the marine model.",
            data=fixed_param_data,
        )
    )

    content.append(html.Div("", id="slider-par1-container"))
    content.append(dbc.Row(style={"height": "10px"}))

    content.append(
        sel.dropdown_with_title(
            "X-Axis Parameter", id="par2-dd", description="Second parameter representing the values for the x-axis."
        )
    )

    par2_row = dbc.Row(
        [
            dbc.Col(
                dmc.NumberInput(
                    id="par2-min",
                    label="Min Value",
                    min=0,
                    step=1,
                    style={"width": "100%"},
                ),
                width=4,
            ),
            dbc.Col(
                dmc.NumberInput(
                    id="par2-max",
                    label="Max Value",
                    min=0,
                    step=1,
                    style={"width": "100%"},
                ),
                width=4,
            ),
            dbc.Col(
                dmc.NumberInput(
                    id="par2-steps",
                    label="Number of Points",
                    value=10,
                    min=1,
                    step=1,
                    max=25,
                    style={"width": "100%"},
                ),
                width=4,
            ),
        ],
        className="g-1",
    )

    content.append(par2_row)

    # Add dropdown for selecting multiple y-axis parameters
    y_axis_params = fixed_param_data + DIC_PARAMS.get_option_list()
    content.append(
        dmc.MultiSelect(
            label="Y-Axis Parameter(s)",
            id="yaxis-multiselect",
            data=y_axis_params,
            value=[],
            maxValues=5,
            searchable=True,
            clearable=True,
            style={"width": "100%"},
        )
    )

    #  Apply and Reset Buttons
    reset_button = sel.button(
        "reset-btn",
        "Reset",
        "ix:reset",
        color=DMC_RED,
    )
    apply_button = sel.button(
        "apply-btn",
        "Apply",
        "ph:play-duotone",
        color=DMC_LIME,
    )

    buttons = dmc.Stack(
        [
            dbc.Row(
                [
                    dbc.Col(reset_button, width=6),
                    dbc.Col(apply_button, width=6),
                ]
            ),
        ]
    )
    content.append(buttons)

    return sel.accordion_with_title(
        "Basic Settings", dmc.Stack(content, align="stretch", gap="xs"), icon="mdi:cog-outline", value="Basic Settings"
    )
