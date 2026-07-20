import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
from core.components import navigation
from core.components.advanced_settings import create_advanced_settings
from core.components.basic_settings import create_basic_settings, create_par1_slider
from core.utils.charts import (
    BJERRUM_PH_MAX,
    BJERRUM_PH_MIN,
    BJERRUM_STEPS,
    create_bjerrum_chart,
    create_line_chart,
    create_line_chart_figure,
    create_speciation_chart,
)
from core.utils.experiments import get_experiment_by_name
from core.utils.layout import get_generic_layout, plot_cell
from core.utils.marine_model import (
    ALKALINITY,
    ALL_PARAMS,
    DIC,
    PH,
    SYSTEM_PARAMS,
    MarineModelParameter,
    run_model_cached,
)
from core.utils.plot_layout import build_plot_flow, default_width, order_keys, width_control
from core.utils.presets import SCHOOL_PRESETS, get_school_preset_by_name
from core.utils.settings import Settings
from dash import ALL, Input, Output, State, callback, ctx, dcc, html
from dash.development.base_component import Component
from flask import request
from locales.translation import TRANSLATION_DICT


dash.register_page(__name__, path="/")

cell_style: dict = {"min-height": "25vh"}


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the Overview page, initialized from the url query parameters.

    :param url_queries: The url arguments, e.g. lang, par1, par1val, par2, min, max, steps, y, sal, temp, sil, phos.
    :return: Layout for the Overview page.
    """
    lang = url_queries.get("lang", "de")
    if lang not in TRANSLATION_DICT:
        lang = "de"

    # School mode only changes the interface, not the model: all controls stay mounted,
    # the technical ones are hidden. Without explicit parameters it opens on the first
    # everyday scenario so students never see an unconfigured app.
    school_mode = url_queries.get("mode") == "schule"
    if school_mode and "par1" not in url_queries:
        settings = SCHOOL_PRESETS[0].settings
    else:
        settings = Settings.from_query(url_queries)

    # A guided experiment loads the disturbed state (from the url) with the baseline
    # conditions frozen as comparison, plus an explanation banner above the plots.
    experiment = get_experiment_by_name(url_queries.get("exp"))
    frozen_data = experiment.frozen_conditions() if experiment else None
    scenario = get_school_preset_by_name(url_queries.get("scen"))

    inputs = [
        dcc.Store(id="lang-store", data=lang),
        dcc.Store(id="mode-store", data="schule" if school_mode else ""),
        dcc.Store(id="frozen-store", data=frozen_data),
        # Remember the plot order (from dragging) and per-tile width. Local storage, so the
        # arrangement survives live updates and a page reload; the reset button clears it.
        dcc.Store(id="plot-order-store", storage_type="local"),
        dcc.Store(id="plot-widths-store", storage_type="local", data={}),
        # Target for the clientside callback that (re)attaches the drag-to-reorder behaviour.
        dcc.Store(id="sortable-dummy"),
        create_basic_settings(
            lang=lang, settings=settings, comparison_active=frozen_data is not None, school_mode=school_mode
        ),
        dbc.Row(html.Div(), className="g-1", style={"height": "18px"}),
        create_advanced_settings(lang=lang, settings=settings, school_mode=school_mode),
        dbc.Row(html.Div(), className="g-1", style={"height": "18px"}),
        dcc.Download(id="download-plot"),
        dcc.Download(id="download-csv"),
    ]

    banner = None
    if experiment is not None:
        banner = dmc.Alert(
            [
                dmc.Text(experiment.description[lang], size="sm"),
                dmc.Anchor(TRANSLATION_DICT[lang]["exp_end"], href=f"/?lang={lang}", size="sm", mt=6),
            ],
            title=experiment.label[lang],
            color="teal",
            radius="md",
            mb=12,
        )
    elif scenario is not None and scenario.question is not None:
        banner = dmc.Alert(
            dmc.Text(scenario.question[lang], size="sm"),
            title=f"{TRANSLATION_DICT[lang]['school_question']}: {scenario.label[lang]}",
            color="teal",
            radius="md",
            mb=12,
        )

    input_layout = dbc.Container(html.Div(id="input-container", children=inputs), style={"width": "100%"}, fluid=True)
    output_layout = dbc.Container(
        [html.Div(children=banner), html.Div(id="plots-container")],
        style={"width": "100%"},
        fluid=True,
    )

    return get_generic_layout(input_layout, output_layout)


def _format_value_with_unit(value: float, unit: str) -> str:
    """Formats a value with its unit, omitting placeholder units.

    :param value: The value to format.
    :param unit: The unit of the value, "-" for unitless parameters.
    :return: Formatted string.
    """
    return f"{value} {unit}" if unit and unit != "-" else f"{value}"


def _build_context_line(
    par1: MarineModelParameter,
    value_par1: float,
    value_salinity: float,
    value_temperature: float,
    value_total_silicate: float,
    value_total_phosphate: float,
    lang: str,
    prefix: str | None = None,
) -> str:
    """Builds a one-line description of the fixed model conditions for plot subtitles and downloads.

    :param par1: The fixed parameter.
    :param value_par1: Value of the fixed parameter.
    :param value_salinity: Value of salinity.
    :param value_temperature: Value of temperature.
    :param value_total_silicate: Value of total silicate.
    :param value_total_phosphate: Value of total phosphate.
    :param lang: Selected language.
    :param prefix: Leading label; defaults to the "fixed" prefix.
    :return: Context line, e.g. "Fest: Gesamtalkalität = 2500 μmol/kg · S = 30 · T = 20 °C · ...".
    """
    dictionary = TRANSLATION_DICT[lang]
    prefix = prefix if prefix is not None else dictionary["context_fixed"]
    parts = [
        f"{prefix}: {par1.label[lang]} = {_format_value_with_unit(value_par1, par1.unit)}",
        f"{dictionary['practical_salinity']} = {value_salinity}",
        f"{dictionary['temperature']} = {value_temperature} °C",
        f"{dictionary['total_silicate']} = {value_total_silicate} μmol/kg",
        f"{dictionary['total_phosphate']} = {value_total_phosphate} μmol/kg",
    ]
    return " · ".join(parts)


@callback(
    [
        Output("plots-container", "children"),
    ],
    [
        Input("apply-btn", "n_clicks"),
        Input("yaxis-multiselect", "value"),
        Input("slider-par1", "value"),
        Input("par2-min", "value"),
        Input("par2-max", "value"),
        Input("par2-steps", "value"),
        Input("slider-salinity", "value"),
        Input("slider-temperature", "value"),
        Input("slider-total-silicate", "value"),
        Input("slider-total_phosphate", "value"),
        Input("frozen-store", "data"),
        Input("bjerrum-switch", "checked"),
        Input("plot-widths-store", "data"),
    ],
    [
        State("par1-dd", "value"),
        State("par2-dd", "value"),
        # The saved order is read, not observed: dragging reorders the DOM directly and only
        # persists to the store, so it must not trigger a rebuild.
        State("plot-order-store", "data"),
        State("lang-store", "data"),
    ],
)
def create_plots(
    n_clicks: int,
    yaxis_names: list[str],
    value_par1: float,
    par2_min_value: float,
    par2_max_value: float,
    par2_steps: int,
    value_salinity: float,
    value_temperature: float,
    value_total_silicate: float,
    value_total_phosphate: float,
    frozen_data: dict | None,
    show_bjerrum: bool,
    widths: dict | None,
    selected_par1_name: str,
    selected_par2_name: str,
    stored_order: list | None,
    lang: str,
) -> tuple[list]:
    """Creates the output plots. Runs on page load and live on every input change (sliders
       report on release, number inputs debounced), so the equilibrium responds immediately.
       A frozen comparison state is drawn as a second gray series in every chart.

    :param n_clicks: Number of apply button clicks (kept as manual fallback trigger).
    :param yaxis_names: Names of the selected y-axis parameters.
    :param value_par1: Value for parameter #1.
    :param par2_min_value: Minimum value for parameter #2.
    :param par2_max_value: Maximum value for parameter #2.
    :param par2_steps: Number of steps for parameter #2.
    :param value_salinity: Value for salinity.
    :param value_temperature: Value for temperature.
    :param value_total_silicate: Value for total silicate.
    :param value_total_phosphate: Value for total phosphate.
    :param frozen_data: Frozen conditions for the comparison mode, or None.
    :param show_bjerrum: Whether to render the Bjerrum plot panel.
    :param widths: Chosen width value per plot key.
    :param selected_par1_name: Name of the selected first parameter.
    :param selected_par2_name: Name of the selected second parameter.
    :param stored_order: The user's saved plot order, or None for the default.
    :param lang: Selected language.
    :return: The plot flow, or a hint if the selection is incomplete.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    dictionary = TRANSLATION_DICT[lang]
    widths = widths or {}

    if not yaxis_names:
        hint = dmc.Alert(
            dictionary["no_yaxis_warning"],
            color="yellow",
            variant="light",
            radius="md",
        )
        return ([hint],)

    par1 = SYSTEM_PARAMS.get_param_by_name(selected_par1_name)
    par2 = SYSTEM_PARAMS.get_param_by_name(selected_par2_name)
    if par1 is None or par2 is None or None in (value_par1, par2_min_value, par2_max_value, par2_steps):
        return (dash.no_update,)

    results = run_model_cached(
        value_par1,
        par1.type,
        par2.type,
        par2_min_value,
        par2_max_value,
        par2_steps,
        value_salinity,
        value_temperature,
        value_total_silicate,
        value_total_phosphate,
    )

    context_line = _build_context_line(
        par1=par1,
        value_par1=value_par1,
        value_salinity=value_salinity,
        value_temperature=value_temperature,
        value_total_silicate=value_total_silicate,
        value_total_phosphate=value_total_phosphate,
        lang=lang,
    )

    # Comparison mode: evaluate the frozen conditions on the current x grid, so both
    # series share the same axis. Only valid while the fixed parameter is unchanged.
    comparison_results = None
    comparison_line = None
    if frozen_data and frozen_data.get("par1_name") == par1.name:
        comparison_results = run_model_cached(
            frozen_data["par1_value"],
            par1.type,
            par2.type,
            par2_min_value,
            par2_max_value,
            par2_steps,
            frozen_data["salinity"],
            frozen_data["temperature"],
            frozen_data["total_silicate"],
            frozen_data["total_phosphate"],
        )
        comparison_line = _build_context_line(
            par1=par1,
            value_par1=frozen_data["par1_value"],
            value_salinity=frozen_data["salinity"],
            value_temperature=frozen_data["temperature"],
            value_total_silicate=frozen_data["total_silicate"],
            value_total_phosphate=frozen_data["total_phosphate"],
            lang=lang,
            prefix=dictionary["comparison_prefix"],
        )

    # Each cell carries a stable key so the flow can remember its order and per-tile width
    # across live updates. The speciation panel comes first: it shows how the equilibrium
    # between the DIC species shifts over the x-axis range.
    def _width_control(key: str) -> Component:
        return width_control(key, widths.get(key, default_width(key)))

    cells = [
        (
            "speciation",
            plot_cell(
                dictionary["speciation_title"],
                html.Div(
                    id="speciation-chart",
                    style=cell_style,
                    children=create_speciation_chart(model_results=results, par_xaxis=par2, lang=lang),
                ),
                subtitle=[dictionary["speciation_hint"], context_line],
                with_download=False,
                header_controls=_width_control("speciation"),
            ),
        )
    ]

    # Optional Bjerrum panel: speciation as a function of pH at the current T and S,
    # with the pH range of the current run marked.
    if show_bjerrum:
        bjerrum_results = run_model_cached(
            2000.0,
            DIC.type,
            PH.type,
            BJERRUM_PH_MIN,
            BJERRUM_PH_MAX,
            BJERRUM_STEPS,
            value_salinity,
            value_temperature,
            value_total_silicate,
            value_total_phosphate,
        )
        current_ph_values = np.atleast_1d(results["pH"]) if par1.name != "pH" else np.atleast_1d(value_par1)
        cells.append(
            (
                "bjerrum",
                plot_cell(
                    dictionary["bjerrum_title"],
                    html.Div(
                        id="bjerrum-chart",
                        style=cell_style,
                        children=create_bjerrum_chart(
                            bjerrum_results=bjerrum_results, current_ph_values=current_ph_values, lang=lang
                        ),
                    ),
                    subtitle=[dictionary["bjerrum_hint"], context_line],
                    with_download=False,
                    header_controls=_width_control("bjerrum"),
                ),
            )
        )

    yaxis_params = [
        ALL_PARAMS.get_param_by_name(name) for name in yaxis_names if ALL_PARAMS.get_param_by_name(name) is not None
    ]
    for yaxis_param in yaxis_params:
        line_chart = create_line_chart(
            model_results=results,
            par_xaxis=par2,
            par_yaxis=yaxis_param,
            lang=lang,
            comparison_results=comparison_results,
            comparison_suffix=dictionary["comparison_suffix"],
        )
        subtitle = context_line
        if yaxis_param.name.startswith("saturation_"):
            subtitle = f"{context_line} · {dictionary['omega_hint']}"
        subtitle_lines = [subtitle] if comparison_line is None else [subtitle, comparison_line]
        key = f"line-{yaxis_param.name}"
        cells.append(
            (
                key,
                plot_cell(
                    dictionary["plot_title_prefix"] + yaxis_param.label[lang],
                    html.Div(id=f"line-chart-{yaxis_param.name}", style=cell_style, children=line_chart),
                    subtitle=subtitle_lines,
                    header_controls=_width_control(key),
                ),
            )
        )

    ordered_cells = dict(cells)
    ordered = [(key, ordered_cells[key]) for key in order_keys(list(ordered_cells), stored_order)]
    flow = build_plot_flow(ordered, widths)
    return ([dmc.Text(dictionary["grid_hint"], size="xs", c="dimmed", mb="xs"), flow],)


@callback(
    Output("plot-widths-store", "data"),
    Input({"type": "tile-width", "key": ALL}, "value"),
    prevent_initial_call=True,
)
def remember_widths(width_values: list[str]) -> dict:
    """Saves the chosen width of every tile when one of the width controls changes.

    :param width_values: The current value of each width control, in id order.
    :return: The width value per plot key.
    """
    widths = {}
    for control in ctx.inputs_list[0]:
        value = control.get("value")
        if value:
            widths[control["id"]["key"]] = value
    return widths


@callback(
    [
        Output("plot-order-store", "data", allow_duplicate=True),
        Output("plot-widths-store", "data", allow_duplicate=True),
    ],
    Input("reset-grid-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_arrangement(n_clicks: int) -> tuple:
    """Clears the saved order and widths, so the plots fall back to their default layout.

    :param n_clicks: Number of clicks on the reset button.
    :return: Empty order and widths.
    """
    return (None, {})


# When the plots are (re)rendered, (re)attach the drag-to-reorder behaviour: SortableJS lets
# the user drag a tile by its header, and on drop it writes the new order back into the store.
dash.clientside_callback(
    """
    function(children) {
        const flow = document.getElementById('plot-flow');
        if (!flow || !window.Sortable) { return window.dash_clientside.no_update; }
        if (flow._sortable) { flow._sortable.destroy(); }
        flow._sortable = window.Sortable.create(flow, {
            handle: '.plot-title-badge',
            draggable: '.plot-tile',
            animation: 150,
            onEnd: function() {
                const order = Array.from(flow.children)
                    .map(child => child.getAttribute('data-key'))
                    .filter(Boolean);
                window.dash_clientside.set_props('plot-order-store', { data: order });
            }
        });
        return window.dash_clientside.no_update;
    }
    """,
    Output("sortable-dummy", "data"),
    Input("plots-container", "children"),
)


@callback(
    [
        Output("frozen-store", "data"),
        Output("freeze-btn", "children"),
    ],
    Input("freeze-btn", "n_clicks"),
    [
        State("frozen-store", "data"),
        State("par1-dd", "value"),
        State("slider-par1", "value"),
        State("slider-salinity", "value"),
        State("slider-temperature", "value"),
        State("slider-total-silicate", "value"),
        State("slider-total_phosphate", "value"),
        State("lang-store", "data"),
    ],
    prevent_initial_call=True,
)
def toggle_comparison(
    n_clicks: int,
    frozen_data: dict | None,
    selected_par1_name: str,
    value_par1: float,
    value_salinity: float,
    value_temperature: float,
    value_total_silicate: float,
    value_total_phosphate: float,
    lang: str,
) -> tuple:
    """Freezes the current conditions for the comparison mode, or ends a running comparison.

    :param n_clicks: Number of clicks on the comparison button.
    :param frozen_data: Currently frozen conditions, or None.
    :param selected_par1_name: Name of the selected first parameter.
    :param value_par1: Value of the first parameter.
    :param value_salinity: Value of salinity.
    :param value_temperature: Value of temperature.
    :param value_total_silicate: Value of total silicate.
    :param value_total_phosphate: Value of total phosphate.
    :param lang: Selected language.
    :return: New frozen store content and the new button label.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    if frozen_data:
        return (None, TRANSLATION_DICT[lang]["compare_start"])

    frozen = {
        "par1_name": selected_par1_name,
        "par1_value": value_par1,
        "salinity": value_salinity,
        "temperature": value_temperature,
        "total_silicate": value_total_silicate,
        "total_phosphate": value_total_phosphate,
    }
    return (frozen, TRANSLATION_DICT[lang]["compare_stop"])


@callback(
    [
        Output("par2-dd", "data"),
        Output("par2-dd", "value"),
    ],
    [
        Input("par1-dd", "value"),
    ],
    [
        State("par2-dd", "value"),
        State("lang-store", "data"),
    ],
    prevent_initial_call=True,
)
def update_par2_dropdown(selected_par1_name: str, selected_par2_name: str, lang: str) -> tuple:
    """Updates the options for the second parameter when the first parameter changes.
       The current selection is kept if it is still valid.

    :param selected_par1_name: Name of the selected first parameter.
    :param selected_par2_name: Name of the currently selected second parameter.
    :param lang: Selected language.
    :return: Options and value for the second parameter.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    par2_options = SYSTEM_PARAMS.get_option_list_without_param(selected_par1_name, lang=lang)

    if selected_par2_name and selected_par2_name != selected_par1_name:
        return (par2_options, dash.no_update)

    fallback = par2_options[0]["value"] if par2_options else None
    return (par2_options, fallback)


@callback(
    [
        Output("yaxis-multiselect", "data"),
        Output("yaxis-multiselect", "value"),
    ],
    [
        Input("par2-dd", "value"),
    ],
    [
        State("yaxis-multiselect", "value"),
        State("lang-store", "data"),
    ],
    prevent_initial_call=True,
)
def update_yaxis_multiselect(selected_par2_name: str, selected_yaxis_names: list[str], lang: str) -> tuple:
    """Updates the options for the y-axis multi-select when the second parameter changes.
       Already selected parameters are kept unless they collide with the x-axis.

    :param selected_par2_name: Name of the selected second parameter.
    :param selected_yaxis_names: Currently selected y-axis parameters.
    :param lang: Selected language.
    :return: Options and value for the y-axis multi-select.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    yaxis_options = ALL_PARAMS.get_option_list_without_param(selected_par2_name, lang=lang)

    kept_names = [name for name in (selected_yaxis_names or []) if name != selected_par2_name]
    if kept_names == (selected_yaxis_names or []):
        return (yaxis_options, dash.no_update)

    return (yaxis_options, kept_names)


@callback(
    [
        Output("par2-min", "value"),
        Output("par2-max", "value"),
        Output("par2-steps", "value"),
    ],
    [
        Input("par2-dd", "value"),
    ],
    prevent_initial_call=True,
)
def update_par2_options(selected_par2_name: str) -> tuple:
    """Resets the x-axis range to the parameter bounds when the second parameter changes.

    :param selected_par2_name: Name of the selected second parameter.
    :return: Min value, max value and number of steps for the second parameter.
    """
    param = SYSTEM_PARAMS.get_param_by_name(selected_par2_name)
    if param is None:
        return (dash.no_update, dash.no_update, dash.no_update)
    return (param.min_value, param.max_value, 10)


@callback(
    Output("slider-par1-container", "children"),
    Input("par1-dd", "value"),
    State("lang-store", "data"),
    prevent_initial_call=True,
)
def update_par1_slider(selected_par1_name: str, lang: str) -> dmc.Slider:
    """Rebuilds the slider for the first parameter when the selected parameter changes.

    :param selected_par1_name: Name of the selected first parameter.
    :param lang: Selected language.
    :return: Slider component for the first parameter.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    param = SYSTEM_PARAMS.get_param_by_name(selected_par1_name)
    if param is None:
        # Fallback to ALKALINITY if not found
        param = ALKALINITY

    return create_par1_slider(param=param, value=param.default_value, lang=lang)


@callback(
    Output("share-clipboard", "content"),
    Input("share-clipboard", "n_clicks"),
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
        State("bjerrum-switch", "checked"),
        State("plot-columns", "value"),
        State("lang-store", "data"),
        State("mode-store", "data"),
    ],
    prevent_initial_call=True,
)
def build_share_link(
    n_clicks: int,
    selected_par1_name: str,
    value_par1: float,
    selected_par2_name: str,
    par2_min_value: float,
    par2_max_value: float,
    par2_steps: int,
    yaxis_names: list[str],
    value_salinity: float,
    value_temperature: float,
    value_total_silicate: float,
    value_total_phosphate: float,
    show_bjerrum: bool,
    plot_columns: str,
    lang: str,
    mode: str,
) -> str:
    """Builds a shareable url containing the current settings; the clipboard component copies it.

    :param n_clicks: Number of clicks on the clipboard icon.
    :param selected_par1_name: Name of the selected first parameter.
    :param value_par1: Value of the first parameter.
    :param selected_par2_name: Name of the selected second parameter.
    :param par2_min_value: Minimum value for the second parameter.
    :param par2_max_value: Maximum value for the second parameter.
    :param par2_steps: Number of steps for the second parameter.
    :param yaxis_names: Names of the selected y-axis parameters.
    :param value_salinity: Value of salinity.
    :param value_temperature: Value of temperature.
    :param value_total_silicate: Value of total silicate.
    :param value_total_phosphate: Value of total phosphate.
    :param show_bjerrum: Whether the Bjerrum plot is shown.
    :param plot_columns: How many plots share a row on wide screens.
    :param lang: Selected language.
    :param mode: Interface mode, "schule" for the reduced school interface.
    :return: Absolute url with all settings as query parameters.
    """
    try:
        columns = int(plot_columns)
    except (TypeError, ValueError):
        columns = 1
    settings = Settings(
        par1_name=selected_par1_name,
        par1_value=value_par1,
        par2_name=selected_par2_name,
        par2_min=par2_min_value,
        par2_max=par2_max_value,
        par2_steps=par2_steps,
        yaxis_names=yaxis_names or [],
        salinity=value_salinity,
        temperature=value_temperature,
        total_silicate=value_total_silicate,
        total_phosphate=value_total_phosphate,
        show_bjerrum=bool(show_bjerrum),
        columns=columns,
    )
    host = request.host_url.rstrip("/")
    mode_query = f"&mode={mode}" if mode else ""
    return f"{host}/?{settings.to_query()}&lang={lang}{mode_query}"


@callback(
    Output("download-csv", "data"),
    Input("csv-btn", "n_clicks"),
    [
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
        State("lang-store", "data"),
    ],
    prevent_initial_call=True,
)
def download_csv(
    n_clicks: int,
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
    lang: str,
) -> dict:
    """Runs the model with the current settings and downloads all results as a CSV file.
       German locale uses semicolon separator and decimal comma so the file opens cleanly in Excel.

    :param n_clicks: Number of clicks on the CSV button.
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
    :return: Dict for dcc.Download with the CSV content.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    par1 = SYSTEM_PARAMS.get_param_by_name(selected_par1_name)
    par2 = SYSTEM_PARAMS.get_param_by_name(selected_par2_name)
    if par1 is None or par2 is None or None in (value_par1, par2_min_value, par2_max_value, par2_steps):
        return dash.no_update

    results = run_model_cached(
        value_par1,
        par1.type,
        par2.type,
        par2_min_value,
        par2_max_value,
        par2_steps,
        value_salinity,
        value_temperature,
        value_total_silicate,
        value_total_phosphate,
    )

    number_of_rows = len(np.atleast_1d(results["par2"]))
    columns = {par2.get_axis_label(lang=lang): np.round(np.atleast_1d(results["par2"]), 4)}
    for param in ALL_PARAMS.params:
        if param.name == par2.name or param.name not in results:
            continue
        values = np.atleast_1d(results[param.name])
        if len(values) == 1:
            values = np.full(number_of_rows, values[0])
        columns[param.get_axis_label(lang=lang)] = np.round(values, 4)

    df = pd.DataFrame(columns)
    separator, decimal = (";", ",") if lang == "de" else (",", ".")
    return dcc.send_data_frame(df.to_csv, "co2ral_results.csv", sep=separator, decimal=decimal, index=False)


@callback(
    Output("navbar-container", "children"),
    Input("url", "search"),
)
def update_navbar(search: str) -> dbc.Navbar:
    """Update the navigation bar based on the url.

    :param search: Current url search, after the ?, e.g., ?lang=de.
    :return: The navigation bar component.
    """
    return navigation.get_navbar(lang=navigation.get_lang_from_search(search))


@callback(
    Output("subtitle-id", "children"),
    Input("lang-segmented", "value"),
    prevent_initial_call=True,
)
def localize_subtitle(lang: str) -> str:
    """Update the subtitle based on the selected language. The url itself is handled by the
       clientside language callback, which reloads the page and keeps all other query parameters.

    :param lang: Selected language.
    :return: Updated subtitle.
    """
    return TRANSLATION_DICT[lang]["app_subtitle"]


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


# Applying a preset means navigating to its url: the option value is the full query string,
# so the page reloads with all controls and plots initialized consistently.
dash.clientside_callback(
    """
    function(value) {
        if (value) {
            const urlParams = new URLSearchParams(window.location.search);
            const lang = urlParams.get('lang') || 'de';
            const mode = urlParams.get('mode');
            const modeQuery = mode ? '&mode=' + mode : '';
            window.location.assign(window.location.pathname + '?' + value + '&lang=' + lang + modeQuery);
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("preset-dd", "data-dummy"),
    Input("preset-dd", "value"),
    prevent_initial_call=True,
)


# Reset navigates to the bare url (keeping only the language), so every control
# returns to its default value and the default plot is rendered.
dash.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            const urlParams = new URLSearchParams(window.location.search);
            const lang = urlParams.get('lang') || 'de';
            const mode = urlParams.get('mode');
            const modeQuery = mode ? '&mode=' + mode : '';
            window.location.assign(window.location.pathname + '?lang=' + lang + modeQuery);
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("reset-btn", "data-dummy"),
    Input("reset-btn", "n_clicks"),
    prevent_initial_call=True,
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
    State("lang-store", "data"),
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
    lang: str,
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
    lang = lang if lang in TRANSLATION_DICT else "de"
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

    results = run_model_cached(
        value_par1,
        par1.type,
        par2.type,
        par2_min_value,
        par2_max_value,
        par2_steps,
        value_salinity,
        value_temperature,
        value_total_silicate,
        value_total_phosphate,
    )

    # Get the y-axis parameter for this plot_id
    yaxis_param = ALL_PARAMS.get_param_by_name(plot_id.split("-")[-1])
    if yaxis_param is None:
        return dash.no_update

    context_line = _build_context_line(
        par1=par1,
        value_par1=value_par1,
        value_salinity=value_salinity,
        value_temperature=value_temperature,
        value_total_silicate=value_total_silicate,
        value_total_phosphate=value_total_phosphate,
        lang=lang,
    )

    # Recreate the figure
    fig = create_line_chart_figure(
        model_results=results, par_xaxis=par2, par_yaxis=yaxis_param, lang=lang, context_line=context_line
    )

    img_bytes = fig.to_image(format="png")
    return dcc.send_bytes(img_bytes, filename=f"co2ral_{plot_id}.png")
