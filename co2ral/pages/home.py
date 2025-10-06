import urllib.parse

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.graph_objs as go
from core.components import navigation
from core.components import selection as sel
from core.components.advanced_settings import create_advanced_settings
from core.components.basic_settings import create_basic_settings
from core.utils.charts import create_line_chart, create_line_chart_figure
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
from dash import ALL, Input, Output, State, callback, ctx, dcc, html
from dash.development.base_component import Component
from locales.translation import TRANSLATION_DICT


(dash.register_page(__name__, path="/"),)

cell_style: dict = {"min-height": "25vh"}


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the Overview page.

    :param url_queries: The url arguments.
    :return: Layout for the Overview page.
    """
    lang = url_queries.get("lang", "de")

    inputs = [
        create_basic_settings(lang=lang),
        dbc.Row(html.Div(), className="g-1", style={"height": "18px"}),
        create_advanced_settings(lang=lang),
        dbc.Row(html.Div(), className="g-1", style={"height": "18px"}),
        dcc.Download(id="download-plot"),
    ]

    input_layout = dbc.Container(html.Div(id="input-container", children=inputs), style={"width": "100%"}, fluid=True)
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
        State("lang-segmented", "value"),
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
    lang: str = "de",
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
    :param lang: Selected language.
    :return: List of go.Figures
    """
    par1 = SYSTEM_PARAMS.get_param_by_name(selected_par1_name)
    par2 = SYSTEM_PARAMS.get_param_by_name(selected_par2_name)
    if par1 is None or par2 is None:
        return ([go.Figure("Not enough parameters selected")],)

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
        line_chart = create_line_chart(model_results=results, par_xaxis=par2, par_yaxis=yaxis_param, lang=lang)
        plots.append(
            plot_cell(
                TRANSLATION_DICT[lang]["plot_title_prefix"] + yaxis_param.label[lang],
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
    [State("lang-segmented", "value")],
)
def update_par2_dropdown_options(selected_par1_name: str, lang: str) -> html.Div:
    """Updates the dropdown value for the second parameter.

    :param selected_par1_name: Name of the selected first parameter.
    :param lang: Selected language.
    :return: List of options for the second parameter.
    """
    par2_params = SYSTEM_PARAMS.get_option_list_without_param(selected_par1_name, lang=lang)

    return (par2_params if par2_params else [],)


@callback(
    [
        Output("yaxis-multiselect", "data"),
    ],
    [
        Input("par2-dd", "value"),
    ],
    [State("lang-segmented", "value")],
)
def update_yaxis_multiselect_options(selected_par2_name: str, lang: str) -> html.Div:
    """Updates the options for the y-axis multi-select based on the second parameter.
    :param selected_par2_name: Name of the selected second parameter.
    :param lang: Selected language.
    :return: List of options for the y-axis multi-select.
    """
    yaxis_params = ALL_PARAMS.get_option_list_without_param(selected_par2_name, lang=lang)
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


@callback(
    Output("slider-par1-container", "children"),
    Input("par1-dd", "value"),
    State("lang-segmented", "value"),
    prevent_initial_call=True,
)
def update_par1_slider(selected_par1_name: str, lang: str) -> dmc.RangeSlider:
    """Updates the range slider for the first parameter based on the selected parameter.

    :param selected_par1_name: Name of the selected first parameter.
    :param lang: Selected language.
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
        name=param.label[lang],
        sub_text=f"Unit: {param.unit}",
        value=param.default_value,
        min_val=min_val,
        max_val=max_val,
        step=step,
    )


@callback(
    Output("navbar-container", "children"),
    Input("url", "search"),
)
def update_navbar(search: str) -> dbc.Navbar:
    """Update the navigation bar based on the url.

    :param search: Current url search, after the ?, e.g., ?lang=de.
    :return: The navigation bar component.
    """
    # Remove leading '?' if present
    query = search[1:] if search and search.startswith("?") else (search or "")
    url_query = dict(urllib.parse.parse_qsl(query))
    lang = url_query.get("lang", "de")

    return navigation.get_navbar(lang=lang)


@callback(
    [
        Output("url", "search"),
        Output("subtitle-id", "children"),
    ],
    Input("lang-segmented", "value"),
    prevent_initial_call=True,
)
def localize_components_and_url(lang: str) -> tuple[str, str]:
    """Update the url based on the selected language.

    :param lang: Selected language.
    :return: Updated url search and subtitle.
    """
    subtitle = TRANSLATION_DICT[lang]["app_subtitle"]
    return f"?lang={lang}", subtitle


dash.clientside_callback(
    """
    function(value) {
        const urlParams = new URLSearchParams(window.location.search);
        const currentLang = urlParams.get('lang') || 'de';
        if (value !== currentLang) {
            urlParams.set('lang', value);
            window.location.search = urlParams.toString();
        }
        return null;
    }
    """,
    Output("lang-segmented", "data-dummy"),
    Input("lang-segmented", "value"),
)


@callback(
    Output("download-plot", "data"),
    Input({"type": "download-btn", "index": ALL}, "n_clicks"),
    State("par1-dd", "value"),
    State("slider-par1", "value"),
    State("par2-dd", "value"),
    State("par2-min", "value"),
    State("par2-max", "value"),
    State("par2-steps", "value"),
    State("slider-salinity", "value"),
    State("slider-temperature", "value"),
    State("slider-total-silicate", "value"),
    State("slider-total_phosphate", "value"),
    State("lang-segmented", "value"),
    prevent_initial_call=True,
)
def download_plot(
    n_clicks_list: list[int],
    selected_par1_name: str,
    value_par1: float,
    selected_par2_name: str,
    par2_min_value: float,
    par2_max_value: float,
    par2_steps: int,
    value_salinity: float,
    value_temperature: float,
    value_total_silicate: float,
    value_total_phosphate: float,
    lang: str = "de",
) -> dict:
    """Download the plot as a PNG file, based on the button clicked call the model
       and recreate the figure as go.Figures.

    :param n_clicks_list: List of button clicks for each download button.
    :param selected_par1_name: Name of the selected first parameter.
    :param value_par1: Value of the first parameter.
    :param selected_par2_name: Name of the selected second parameter.
    :param par2_min_value: Minimum value for the second parameter.
    :param par2_max_value: Maximum value for the second parameter.
    :param par2_steps: Number of steps for the second parameter.
    :param value_salinity: Value of salinity.
    :param value_temperature: Value of temperature.
    :param value_total_silicate: Value of total silicate.
    :param value_total_phosphate: Value of total phosphate.
    :param lang: Selected language.
    :return: Dict with content and filename for dcc.send_bytes.
    """
    triggered = ctx.triggered_id
    if not triggered:
        return dash.no_update

    plot_id = triggered["index"]
    for i, input_dict in enumerate(ctx.inputs_list[0]):
        if input_dict["id"]["index"] == plot_id:
            if n_clicks_list[i] is None or n_clicks_list[i] == 0:
                return dash.no_update
            break

    # Recreate the model
    par1 = SYSTEM_PARAMS.get_param_by_name(selected_par1_name)
    par2 = SYSTEM_PARAMS.get_param_by_name(selected_par2_name)
    if par1 is None or par2 is None:
        return dash.no_update

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

    # Get the y-axis parameter for this plot_id
    yaxis_param = ALL_PARAMS.get_param_by_name(plot_id.split("-")[-1])
    if yaxis_param is None:
        return dash.no_update

    # Recreate the figure
    fig = create_line_chart_figure(model_results=results, par_xaxis=par2, par_yaxis=yaxis_param, lang=lang)

    img_bytes = fig.to_image(format="png")
    return dcc.send_bytes(img_bytes, filename=f"co2ral_{plot_id}.png")
