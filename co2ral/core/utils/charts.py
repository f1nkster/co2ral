import dash_mantine_components as dmc
import numpy as np
from core.utils.marine_model import MarineModelParameter


def create_line_chart(
    model_results: dict,
    par_xaxis: MarineModelParameter,
    par_yaxis: MarineModelParameter,
) -> dmc.LineChart:
    """Creates a line chart for given model parameters.

    :param model_results: Result dict.
    :param par_xaxis: Parameter for x axis.
    :param par_yaxis: Parameter for y axis.
    :return: Line chart.
    """
    # Get the x and y values for the plot
    x_values = np.round(model_results["par2"], 2)
    y_values = np.round(model_results[par_yaxis.name], 2)

    data = [{"x": x, par_yaxis.label: y} for (x, y) in zip(x_values, y_values, strict=False)]
    series = [{"name": par_yaxis.label, "color": "indigo.6"}]

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
        yAxisLabel=par_yaxis.get_axis_label(),
    )

    return line_chart
