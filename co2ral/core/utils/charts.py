from typing import Optional

import dash_mantine_components as dmc
from core.utils.marine_model import MarineModelParameter


def create_line_chart(
    model_results: dict,
    par_xaxis: MarineModelParameter,
    par_yaxis_left: MarineModelParameter,
    par_yaxis_right: Optional[MarineModelParameter] = None,
) -> dmc.LineChart:
    """Creates a line chart for given model parameters.

    :param model_results: Result dict.
    :param par_xaxis: Parameter for x axis.
    :param par_yaxis_left: Parameter for left y axis.
    :param par_yaxis_right: Parameter for right y axis, defaults to None
    :return: Line chart.
    """
    # Get the x and y values for the plot
    x_values = model_results["par2"]
    y_values_left = model_results[par_yaxis_left.name]
    if par_yaxis_right:
        y_values_right = model_results[par_yaxis_right.name]
        data = [
            {"x": x, par_yaxis_left.label: y_left, par_yaxis_right.label: y_right}
            for (x, y_left, y_right) in zip(x_values, y_values_left, y_values_right, strict=False)
        ]
        series = [
            {"name": par_yaxis_left.label, "color": "indigo.6"},
            {"name": par_yaxis_right.label, "color": "cyan.6", "yAxisId": "right"},
        ]
    else:
        data = [{"x": x, par_yaxis_left.label: y} for (x, y) in zip(x_values, y_values_left, strict=False)]
        series = [{"name": par_yaxis_left.label, "color": "indigo.6"}]

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
        xAxisLabel=par_xaxis.get_axis_label(),
        yAxisLabel=par_yaxis_left.get_axis_label(),
        rightYAxisLabel=par_yaxis_right.get_axis_label() if par_yaxis_right else None,
        withRightYAxis=True if par_yaxis_right else False,
    )

    return line_chart
