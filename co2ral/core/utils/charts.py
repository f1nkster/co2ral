import dash_mantine_components as dmc
import numpy as np
import plotly.graph_objs as go
from core.utils.marine_model import MarineModelParameter


def create_line_chart(
    model_results: dict,
    par_xaxis: MarineModelParameter,
    par_yaxis: MarineModelParameter,
    lang: str = "de",
) -> dmc.LineChart:
    """Creates a line chart for given model parameters.

    :param model_results: Result dict.
    :param par_xaxis: Parameter for x axis.
    :param par_yaxis: Parameter for y axis.
    :param lang: Language for labels.
    :return: Line chart.
    """
    # Get the x and y values for the plot
    x_values = np.round(model_results["par2"], 2)
    y_values = np.round(model_results[par_yaxis.name], 2)

    data = [{"x": x, par_yaxis.label[lang]: y} for (x, y) in zip(x_values, y_values, strict=False)]
    series = [{"name": par_yaxis.label[lang], "color": "indigo.6"}]

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
    return fig
