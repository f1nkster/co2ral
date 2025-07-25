import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.graph_objs as go
from core.components import selection as sel
from core.utils.charts import create_line_chart
from core.utils.layout import get_generic_layout, plot_cell
from core.utils.marine_model import (
    ALKALINITY,
    CO3,
    DIC,
    HCO3,
    PCO2,
    PH,
    SALINITY,
    TEMPERATURE,
    TOTAL_PHOSPHATE,
    TOTAL_SILICATE,
    MarineModel,
)
from dash import callback, html
from dash.dependencies import Input, Output, State
from dash.development.base_component import Component
from env.colors import DMC_LIME, DMC_RED


(dash.register_page(__name__, path="/"),)

cell_style: dict = {"min-height": "25vh"}


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the Overview page.

    :param url_queries: The url arguments.
    :return: Layout for the Overview page.
    """
    content = []

    ### Carbonate System Parameters
    content.append(sel.badge("Carbonate System Parameters"))
    par1 = ALKALINITY
    par1_slider = sel.range_slider(
        id="slider-par1",
        name=par1.label,
        sub_text=f"Unit: {par1.unit}",
        value=par1.default_value,
        min_val=2300,
        max_val=2500,
        step=10,
    )
    content.append(par1_slider)
    content.append(dbc.Row(style={"height": "10px"}))

    content.append(dbc.Row(style={"height": "30px"}))

    ### Hydrographic Conditions
    content.append(sel.badge("Hydrographic Conditions"))

    salinity_slider = sel.range_slider(
        id="slider-salinity", name="Practical Salinity", sub_text="Unit: -", value=35, min_val=10, max_val=50, step=1
    )

    content.append(salinity_slider)
    content.append(dbc.Row(style={"height": "10px"}))

    temperature_slider = sel.range_slider(
        id="slider-temperature", name="Temperature", sub_text="Unit: °C", value=25, min_val=5, max_val=40, step=1
    )

    content.append(temperature_slider)
    content.append(dbc.Row(style={"height": "10px"}))

    content.append(dbc.Row(style={"height": "30px"}))

    ### Nutrients
    content.append(sel.badge("Nutrients"))
    total_silicate_slider = sel.range_slider(
        id="slider-total-silicate",
        name="Total Silicate",
        sub_text="Unit: μmol/kg",
        value=25,
        min_val=5,
        max_val=40,
        step=1,
    )
    content.append(total_silicate_slider)
    content.append(dbc.Row(style={"height": "10px"}))
    total_phosphate_slider = sel.range_slider(
        id="slider-total_phosphate",
        name="Total Phosphate",
        sub_text="Unit: μmol/kg",
        value=25,
        min_val=5,
        max_val=40,
        step=1,
    )
    content.append(total_phosphate_slider)
    content.append(dbc.Row(style={"height": "10px"}))

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
            sel.badge("Action"),
            dbc.Row(
                [
                    dbc.Col(reset_button, width=6),
                    dbc.Col(apply_button, width=6),
                ]
            ),
        ]
    )
    content.append(buttons)

    input_layout = [
        sel.accordion_with_title(
            "Controls",
            dmc.Stack(content, align="stretch", gap="xs"),
            icon="mdi:database-cog",
        ),
        dbc.Row(html.Div(), className="g-1", style={"height": "18px"}),
        # TODO: Add advanced settings
    ]

    output_layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(plot_cell("Plot #1", html.Div(id="line-chart", style=cell_style)), width=12),
                ],
                className="g-1",
            ),
            dbc.Row(html.Div(), className="g-1", style={"height": "18px"}),
            dbc.Row(
                [
                    dbc.Col(plot_cell("Plot #2", html.Div(id="line-chart-2", style=cell_style)), width=12),
                ],
                className="g-1",
            ),
        ],
        fluid=True,
    )
    return get_generic_layout(input_layout, output_layout)


@callback(
    [
        Output("line-chart", "children"),
        Output("line-chart-2", "children"),
    ],
    [Input("apply-btn", "n_clicks")],
    [
        State("slider-par1", "value"),
        State("slider-salinity", "value"),
        State("slider-temperature", "value"),
        State("slider-total-silicate", "value"),
        State("slider-total_phosphate", "value"),
    ],
)
def update_output(
    n_clicks: int,
    value_par1: int,
    value_salinity: int,
    value_temperature: int,
    value_total_silicate: int,
    value_total_phosphate: int,
) -> tuple[go.Figure, go.Figure]:
    """Updates the output

    :param n_clicks: Number of button click
    :param value_par1: Value for parameter #1
    :param value_salinity: Value for salinity
    :param value_temperature: Value for salinity
    :param value_total_silicate: Value for total silicate
    :param value_total_phosphate: Value for total phosphate
    :return: Figures
    """
    # Init the model with the user input and run it
    model = MarineModel(
        value_par1=value_par1,
        value_salinity=value_salinity,
        value_temperature=value_temperature,
        value_total_silicate=value_total_silicate,
        value_total_phosphate=value_total_phosphate,
    )
    results = model.run()

    line_chart = create_line_chart(model_results=results, par_xaxis=DIC, par_yaxis_left=PCO2, par_yaxis_right=PH)
    line_chart_2 = create_line_chart(model_results=results, par_xaxis=DIC, par_yaxis_left=CO3, par_yaxis_right=HCO3)

    return (line_chart,), (line_chart_2,)


@callback(
    [
        Output("slider-par1", "value"),
        Output("slider-salinity", "value"),
        Output("slider-temperature", "value"),
        Output("slider-total-silicate", "value"),
        Output("slider-total_phosphate", "value"),
    ],
    [Input("reset-btn", "n_clicks")],
)
def set_default_values(n_clicks: int) -> tuple:
    """Reset the slider values to default parameters.

    :param n_clicks: Number of button click
    :return: Tuple of default values.
    """
    if n_clicks is None:
        return

    value_par1 = ALKALINITY.default_value
    value_salinity = SALINITY.default_value
    value_temperature = TEMPERATURE.default_value
    value_total_silicate = TOTAL_SILICATE.default_value
    value_total_phosphate = TOTAL_PHOSPHATE.default_value

    return (value_par1, value_salinity, value_temperature, value_total_silicate, value_total_phosphate)
