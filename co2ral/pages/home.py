import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.graph_objs as go
from core.components import selection as sel
from core.components.settings import create_basic_settings
from core.utils.charts import create_line_chart
from core.utils.layout import get_generic_layout, plot_cell
from core.utils.marine_model import (
    ALKALINITY,
    ALL_PARAMS,
    SALINITY,
    SYSTEM_PARAMS,
    TEMPERATURE,
    TOTAL_PHOSPHATE,
    TOTAL_SILICATE,
    MarineModel,
)
from dash import callback, html
from dash.dependencies import Input, Output, State
from dash.development.base_component import Component


(dash.register_page(__name__, path="/"),)

cell_style: dict = {"min-height": "25vh"}


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the Overview page.

    :param url_queries: The url arguments.
    :return: Layout for the Overview page.
    """
    content = []

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
        value=TOTAL_SILICATE.default_value,
        min_val=TOTAL_SILICATE.min_value,
        max_val=TOTAL_SILICATE.max_value,
        step=1,
    )
    content.append(total_silicate_slider)
    content.append(dbc.Row(style={"height": "10px"}))
    total_phosphate_slider = sel.range_slider(
        id="slider-total_phosphate",
        name="Total Phosphate",
        sub_text="Unit: μmol/kg",
        value=TOTAL_PHOSPHATE.default_value,
        min_val=TOTAL_PHOSPHATE.min_value,
        max_val=TOTAL_PHOSPHATE.max_value,
        step=1,
    )
    content.append(total_phosphate_slider)
    content.append(dbc.Row(style={"height": "10px"}))

    input_layout = [
        create_basic_settings(),
        dbc.Row(html.Div(), className="g-1", style={"height": "18px"}),
        sel.accordion_with_title(
            "Advanced Settings",
            dmc.Stack(content, align="stretch", gap="xs"),
            icon="mdi:database-cog",
        ),
        dbc.Row(html.Div(), className="g-1", style={"height": "18px"}),
        # TODO: Add advanced settings
    ]

    output_layout = dbc.Container(html.Div(id="plots-container"), style={"width": "100%"}, fluid=True)

    return get_generic_layout(input_layout, output_layout)


@callback(
    [
        Output("plots-container", "children"),
    ],
    [Input("apply-btn", "n_clicks")],
    [
        State("par1-dd", "value"),
        State("slider-par1", "value"),
        State("par2-dd", "value"),
        State("par2-min", "value"),
        State("par2-max", "value"),
        State("par2-steps", "value"),
        State("yaxis-multiselect", "value"),
        State("slider-salinity", "value"),
        State("slider-temperature", "value"),
        State("slider-total-silicate", "value"),
        State("slider-total_phosphate", "value"),
    ],
    prevent_initial_call=True,
)
def update_output(
    n_clicks: int,
    selected_par1_name: str,
    value_par1: int,
    selected_par2_name: str,
    par2_min_value: int,
    par2_max_value: int,
    par2_steps: int,
    yaxis_names: list[str],
    value_salinity: int,
    value_temperature: int,
    value_total_silicate: int,
    value_total_phosphate: int,
) -> tuple[list[go.Figure]]:
    """Updates the output

    :param n_clicks: Number of button click
    :param selected_par1_name: Name of the selected first parameter.
    :param value_par1: Value for parameter #1
    :param selected_par2_name: Name of the selected second parameter.
    :param par2_min_value: Minimum value for parameter
    :param par2_max_value: Maximum value for parameter
    :param par2_steps: Number of steps for parameter
    :param yaxis_names: Names of the selected y-axis parameters
    :param value_salinity: Value for salinity
    :param value_temperature: Value for temperature
    :param value_total_silicate: Value for total silicate
    :param value_total_phosphate: Value for total phosphate
    :return: Figures
    """
    par1 = SYSTEM_PARAMS.get_param_by_name(selected_par1_name)
    par2 = SYSTEM_PARAMS.get_param_by_name(selected_par2_name)
    if par1 is None or par2 is None:
        return (go.Figure("Not enough parameters selected"),)

    # Init the model with the user input and run it
    model = MarineModel(
        value_par1=value_par1,
        type_par1=par1.type,
        type_par2=par2.type,
        min_value_par2=par2_min_value,
        max_value_par2=par2_max_value,
        number_of_steps=par2_steps,
        value_salinity=value_salinity,
        value_temperature=value_temperature,
        value_total_silicate=value_total_silicate,
        value_total_phosphate=value_total_phosphate,
    )
    results = model.run()

    plots = []
    yaxis_params = [
        ALL_PARAMS.get_param_by_name(name) for name in yaxis_names if ALL_PARAMS.get_param_by_name(name) is not None
    ]
    for yaxis_param in yaxis_params:
        line_chart = create_line_chart(model_results=results, par_xaxis=par2, par_yaxis=yaxis_param)
        plots.append(
            plot_cell(
                f"Plot for {yaxis_param.name}",
                html.Div(id=f"line-chart-{yaxis_param.name}", style=cell_style, children=line_chart),
            )
        )

    return (plots,)


@callback(
    [
        Output("par1-dd", "value"),
    ],
    [
        Input("par1-dd", "data"),
    ],
)
def update_par1_dropdown_value(par1_options: dict) -> html.Div:
    """Updates the dropdown value for the first parameter.

    :param par1_options: List of options for the first parameter.
    :return: Name of the first parameter.
    """
    if par1_options:
        return (par1_options[0]["value"],)


@callback(
    [
        Output("par2-dd", "data"),
    ],
    [
        Input("par1-dd", "value"),
    ],
)
def update_par2_dropdown_options(selected_par1_name: str) -> html.Div:
    """Updates the dropdown value for the second parameter.
    :param selected_par1_name: Name of the selected first parameter.
    :return: List of options for the second parameter.
    """
    par2_params = SYSTEM_PARAMS.get_option_list_without_param(selected_par1_name)

    return (par2_params if par2_params else [],)


@callback(
    [
        Output("yaxis-multiselect", "data"),
    ],
    [
        Input("par2-dd", "value"),
    ],
)
def update_yaxis_multiselect_options(selected_par2_name: str) -> html.Div:
    """Updates the options for the y-axis multi-select based on the second parameter.
    :param selected_par2_name: Name of the selected second parameter.
    :return: List of options for the y-axis multi-select.
    """
    yaxis_params = ALL_PARAMS.get_option_list_without_param(selected_par2_name)
    return (yaxis_params if yaxis_params else [],)


@callback(
    [
        Output("par2-dd", "value"),
    ],
    [
        Input("par2-dd", "data"),
    ],
)
def update_par2_dropdown_value(par2_options: dict) -> html.Div:
    """Updates the dropdown value for the second parameter.

    :param par2_options: List of options for the second parameter.
    :return: Name of the second parameter.
    """
    if par2_options:
        param = SYSTEM_PARAMS.get_param_by_name(par2_options[0]["value"])
        return (param.name,)


@callback(
    [
        Output("par2-min", "value"),
        Output("par2-max", "value"),
        Output("par2-steps", "value"),
    ],
    [
        Input("par2-dd", "value"),
    ],
)
def update_par2_options(selected_par2_name: str) -> html.Div:
    """Updates the options for the second parameter based on the first parameter.
    :param selected_par2_name: Name of the selected second parameter.
    :return: List of options for the second parameter.
    """
    param = SYSTEM_PARAMS.get_param_by_name(selected_par2_name)
    if param is None:
        return []
    return (param.min_value, param.max_value, 10)


@callback(
    [
        Output("slider-par1", "value"),
        Output("slider-salinity", "value"),
        Output("slider-temperature", "value"),
        Output("slider-total-silicate", "value"),
        Output("slider-total_phosphate", "value"),
    ],
    [
        Input("reset-btn", "n_clicks"),
    ],
    [
        State("par1-dd", "value"),
    ],
    prevent_initial_call=True,
)
def set_default_values(n_clicks: int, selected_par1_name: str) -> tuple:
    """Reset the slider values to default parameters.

    :param n_clicks: Number of button click
    :param selected_par1_name: Name of the selected first parameter.
    :return: Tuple of default values.
    """
    if n_clicks is None:
        return

    param = SYSTEM_PARAMS.get_param_by_name(selected_par1_name)
    if param is None:
        # Fallback to ALKALINITY if not found
        param = ALKALINITY

    value_par1 = param.default_value
    value_salinity = SALINITY.default_value
    value_temperature = TEMPERATURE.default_value
    value_total_silicate = TOTAL_SILICATE.default_value
    value_total_phosphate = TOTAL_PHOSPHATE.default_value

    return (value_par1, value_salinity, value_temperature, value_total_silicate, value_total_phosphate)


@callback(Output("slider-par1-container", "children"), Input("par1-dd", "value"), prevent_initial_call=True)
def update_par1_slider(selected_par1_name: str) -> dmc.RangeSlider:
    """Updates the range slider for the first parameter based on the selected parameter.

    :param selected_par1_name: Name of the selected first parameter.
    :return: Range slider component for the first parameter.
    """
    param = SYSTEM_PARAMS.get_param_by_name(selected_par1_name)
    if param is None:
        # Fallback to ALKALINITY if not found
        param = ALKALINITY

    min_val = param.min_value
    max_val = param.max_value
    step = 10 if param.unit == "μmol/kg" else 1

    return sel.range_slider(
        id="slider-par1",
        name=param.label,
        sub_text=f"Unit: {param.unit}",
        value=param.default_value,
        min_val=min_val,
        max_val=max_val,
        step=step,
    )
