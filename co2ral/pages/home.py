import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import numpy as np
import plotly.graph_objs as go
import PyCO2SYS
from core.components import selection as sel
from core.utils.layout import get_generic_layout, plot_cell
from dash import callback, html
from dash.dependencies import Input, Output
from dash.development.base_component import Component


(dash.register_page(__name__, path="/"),)

cell_style: dict = {"min-height": "25vh"}

salinity = 35
temperature = 25
total_silicate = 50
total_phosphate = 2
par1 = 2400
kwargs = {
    "par1": par1,  # Value of the first parameter
    "par2": np.arange(2000, 3001, 250),  # Value of the second parameter, which is a long vector of different DIC's!
    "par1_type": 1,  # The first parameter supplied is of type "1", which is "alkalinity"
    "par2_type": 2,  # The second parameter supplied is of type "2", which is "DIC"
    "salinity": salinity,  # Salinity of the sample
    "temperature": temperature,  # Temperature at input conditions
    "total_silicate": total_silicate,  # Concentration of silicate  in the sample (in umol/kg)
    "total_phosphate": total_phosphate,  # Concentration of phosphate in the sample (in umol/kg)
    "opt_k_carbonic": 4,  # Choice of H2CO3 and HCO3- dissociation constants K1 and K2 ("4" means "Mehrbach refit")
    "opt_k_bisulfate": 1,  # Choice of HSO4- dissociation constants KSO4 ("1" means "Dickson")
}


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the Overview page.

    :param url_queries: The url arguments.
    :return: Layout for the Overview page.
    """
    content = []

    par1_slider = sel.range_slider(
        id="slider-par1",
        name="Total Alkalinity",
        sub_text="Unit: μmol/kg",
        value=2400,
        min_val=2300,
        max_val=2500,
        step=10,
    )

    content.append(sel.badge("Carbonate System Parameters"))
    content.append(par1_slider)
    content.append(dbc.Row(style={"height": "10px"}))

    content.append(dbc.Row(style={"height": "30px"}))
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

    input_layout = sel.accordion_with_title(
        "Controls",
        dmc.Stack(content, align="stretch", gap="xs"),
        icon="mdi:database-cog",
    )

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
    [Output("line-chart", "children"), Output("line-chart-2", "children")],
    [
        Input("slider-par1", "value"),
        Input("slider-salinity", "value"),
        Input("slider-temperature", "value"),
        Input("slider-total-silicate", "value"),
        Input("slider-total_phosphate", "value"),
    ],
)
def update_output(
    value_par1: int, value_salinity: int, value_temperature: int, value_total_silicate: int, value_total_phosphate: int
) -> tuple[go.Figure, go.Figure]:
    """Updates the output

    :param value_par1: Value for parameter #1
    :param value_salinity: Value for salinity
    :param value_temperature: Value for salinity
    :param value_total_silicate: Value for total silicate
    :param value_total_phosphate: Value for total phosphate
    :return: Test
    """
    kwargs["par1"] = value_par1
    kwargs["salinity"] = value_salinity
    kwargs["temperature"] = value_temperature
    kwargs["total_silicate"] = value_total_silicate
    kwargs["total_phosphate"] = value_total_phosphate

    # Run CO2SYS!
    results = PyCO2SYS.sys(**kwargs)

    # ("par2", "pCO2", data=results, c="r", marker="o")

    # Define the data for your line plot
    x_values = results["par2"]
    y_values = results["pCO2"]
    y_values_2 = results["pH"]

    co3 = results["CO3"]
    hco3 = results["HCO3"]

    fig = go.Figure(data=[go.Scatter(x=x_values, y=y_values)])
    fig.update_layout(title="", xaxis_title="DIC [umol/kg]", yaxis_title="pCO2 [uatm]")

    data = [{"x": x, "pCO2": y, "pH": y2} for (x, y, y2) in zip(x_values, y_values, y_values_2, strict=False)]
    line_chart = dmc.LineChart(
        h=300,
        dataKey="x",
        data=data,
        series=[{"name": "pCO2", "color": "indigo.6"}, {"name": "pH", "color": "cyan.6", "yAxisId": "right"}],
        curveType="natural",
        tickLine="xy",
        withXAxis=True,
        withDots=True,
        withLegend=True,
        xAxisLabel="DIC [umol/kg]",
        yAxisLabel="pCO2 [uatm]",
        rightYAxisLabel="pH",
        withRightYAxis=True,
    )

    fig_2 = go.Figure(data=[go.Scatter(x=x_values, y=y_values_2)])
    fig_2.update_layout(title="", xaxis_title="DIC [umol/kg]", yaxis_title="pH")

    data_2 = [{"x": x, "CO3": y, "HCO3": y2} for (x, y, y2) in zip(x_values, co3, hco3, strict=False)]
    line_chart_2 = dmc.LineChart(
        h=300,
        dataKey="x",
        data=data_2,
        series=[{"name": "CO3", "color": "indigo.6"}, {"name": "HCO3", "color": "cyan.6", "yAxisId": "right"}],
        curveType="natural",
        tickLine="xy",
        withXAxis=True,
        withDots=True,
        withLegend=True,
        xAxisLabel="DIC [μmol/kg]",
        yAxisLabel="CO3 [μmol/kg]",
        rightYAxisLabel="HCO3 [μmol/kg]",
        withRightYAxis=True,
    )

    # return (line_chart, ), (html.Div(dcc.Graph(figure=fig_2)), )
    return (line_chart,), (line_chart_2,)
