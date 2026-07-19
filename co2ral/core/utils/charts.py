import dash_mantine_components as dmc
import numpy as np
import plotly.graph_objs as go
from core.utils.marine_model import SPECIATION_PARAMS, MarineModelParameter


SPECIATION_COLORS = ["orange.6", "blue.6", "teal.6"]


def _is_saturation_param(param: MarineModelParameter) -> bool:
    """Checks whether a parameter is a saturation state (Ω).

    :param param: Parameter to check.
    :return: True for aragonite/calcite saturation.
    """
    return param.name.startswith("saturation_")


def create_line_chart(
    model_results: dict,
    par_xaxis: MarineModelParameter,
    par_yaxis: MarineModelParameter,
    lang: str = "de",
    comparison_results: dict | None = None,
    comparison_suffix: str = "",
) -> dmc.LineChart:
    """Creates a line chart for given model parameters. Saturation states (Ω) get a
       reference line at Ω = 1, the threshold between calcification and dissolution.
       If comparison results are given, they are drawn as a second gray series.

    :param model_results: Result dict.
    :param par_xaxis: Parameter for x axis.
    :param par_yaxis: Parameter for y axis.
    :param lang: Language for labels.
    :param comparison_results: Result dict of a frozen state, evaluated on the same x grid.
    :param comparison_suffix: Suffix for the comparison series name, e.g. " (Vergleich)".
    :return: Line chart.
    """
    # Get the x and y values for the plot
    x_values = np.round(model_results["par2"], 2)
    y_values = np.round(model_results[par_yaxis.name], 2)

    data = [{"x": x, par_yaxis.label[lang]: y} for (x, y) in zip(x_values, y_values, strict=False)]
    series = [{"name": par_yaxis.label[lang], "color": "indigo.6"}]

    if comparison_results is not None:
        comparison_name = par_yaxis.label[lang] + comparison_suffix
        comparison_values = np.round(comparison_results[par_yaxis.name], 2)
        for row, y_comparison in zip(data, comparison_values, strict=False):
            row[comparison_name] = y_comparison
        series.append({"name": comparison_name, "color": "gray.6"})

    # extendDomain keeps the Ω = 1 threshold visible even when all data points lie above or below it.
    reference_lines = (
        [{"y": 1, "label": "Ω = 1", "color": "red.6", "strokeDasharray": "5 5", "ifOverflow": "extendDomain"}]
        if _is_saturation_param(par_yaxis)
        else []
    )

    line_chart = dmc.LineChart(
        h=300,
        dataKey="x",
        data=data,
        series=series,
        curveType="natural",
        tickLine="xy",
        withXAxis=True,
        withDots=True,
        withLegend=True,
        xAxisLabel=par_xaxis.get_axis_label(lang=lang),
        yAxisLabel=par_yaxis.get_axis_label(lang=lang),
        # Scale both axes to the data range instead of starting at zero,
        # so small but meaningful changes (e.g. pH 8.3 -> 7.8) become clearly visible.
        xAxisProps={"type": "number", "domain": ["auto", "auto"]},
        yAxisProps={"domain": ["auto", "auto"]},
        referenceLines=reference_lines,
    )

    return line_chart


def create_line_chart_figure(
    model_results: dict,
    par_xaxis: MarineModelParameter,
    par_yaxis: MarineModelParameter,
    lang: str = "de",
    context_line: str | None = None,
) -> go.Figure:
    """Creates a line chart figure for given model parameters.

    :param model_results: Result dict.
    :param par_xaxis: Parameter for x axis.
    :param par_yaxis: Parameter for y axis.
    :param lang: Language for labels, defaults to "de"
    :param context_line: Text describing the fixed model conditions, shown as figure title
    :return: Line chart figure as go.Figure.
    """
    x_values = np.round(model_results["par2"], 2)
    y_values = np.round(model_results[par_yaxis.name], 2)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines+markers",
            name=par_yaxis.label[lang],
            line={"color": "indigo"},
        )
    )
    fig.update_layout(
        xaxis_title=par_xaxis.get_axis_label(lang=lang),
        yaxis_title=par_yaxis.get_axis_label(lang=lang),
        height=300,
        legend={"orientation": "h"},
        margin={"l": 40, "r": 20, "t": 60 if context_line else 40, "b": 40},
    )
    if context_line:
        fig.update_layout(title={"text": context_line, "font": {"size": 11}, "x": 0.5, "xanchor": "center"})
    if _is_saturation_param(par_yaxis):
        fig.add_hline(y=1, line_dash="dash", line_color="red", annotation_text="Ω = 1")
    return fig


def create_speciation_chart(
    model_results: dict,
    par_xaxis: MarineModelParameter,
    lang: str = "de",
) -> dmc.AreaChart:
    """Creates a 100 % stacked area chart of the DIC speciation (CO₂(aq), HCO₃⁻, CO₃²⁻)
       over the x-axis range — the central visualization of the shifting equilibrium.

    :param model_results: Result dict.
    :param par_xaxis: Parameter for x axis.
    :param lang: Language for labels.
    :return: Stacked percent area chart.
    """
    x_values = np.round(model_results["par2"], 2)

    data = []
    for i, x in enumerate(x_values):
        row = {"x": x}
        for param in SPECIATION_PARAMS:
            row[param.label[lang]] = float(np.round(np.atleast_1d(model_results[param.name])[i], 2))
        data.append(row)

    series = [
        {"name": param.label[lang], "color": color}
        for param, color in zip(SPECIATION_PARAMS, SPECIATION_COLORS, strict=False)
    ]

    return dmc.AreaChart(
        h=300,
        dataKey="x",
        data=data,
        series=series,
        type="percent",
        curveType="natural",
        withXAxis=True,
        withLegend=True,
        withDots=False,
        xAxisLabel=par_xaxis.get_axis_label(lang=lang),
        xAxisProps={"type": "number", "domain": ["auto", "auto"]},
    )
