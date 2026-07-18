import numpy as np
from core.utils.charts import create_line_chart, create_line_chart_figure
from core.utils.marine_model import DIC, OMEGA_ARAGONITE, PCO2, PH


def _fake_results() -> dict:
    """Builds a minimal model result dict for chart tests.

    :return: Result dict with a DIC range and matching pH values.
    """
    return {"par2": np.linspace(1800, 2400, 5), "pH": np.linspace(8.4, 7.6, 5)}


def test__create_line_chart__axes_scale_to_data():
    """GIVEN model results with a narrow pH range
    WHEN the line chart is created
    THEN both axes use a data-driven domain instead of starting at zero
    """
    chart = create_line_chart(model_results=_fake_results(), par_xaxis=DIC, par_yaxis=PH, lang="de")

    assert chart.yAxisProps["domain"] == ["auto", "auto"]
    assert chart.xAxisProps["domain"] == ["auto", "auto"]
    assert chart.xAxisProps["type"] == "number"


def test__create_line_chart__contains_all_data_points():
    """GIVEN model results
    WHEN the line chart is created
    THEN every model step appears as a data point with the localized series key
    """
    chart = create_line_chart(model_results=_fake_results(), par_xaxis=DIC, par_yaxis=PH, lang="de")

    assert len(chart.data) == 5
    assert chart.data[0]["x"] == 1800
    assert chart.data[0][PH.label["de"]] == 8.4


def test__create_line_chart__saturation_param_gets_omega_reference_line():
    """GIVEN a saturation state as y-axis parameter
    WHEN the line chart is created
    THEN a reference line at Ω = 1 is added, while other parameters get none
    """
    results = {"par2": np.linspace(280, 1000, 5), "saturation_aragonite": np.linspace(3.5, 1.2, 5)}

    omega_chart = create_line_chart(model_results=results, par_xaxis=PCO2, par_yaxis=OMEGA_ARAGONITE, lang="de")
    ph_chart = create_line_chart(model_results=_fake_results(), par_xaxis=DIC, par_yaxis=PH, lang="de")

    assert len(omega_chart.referenceLines) == 1
    assert omega_chart.referenceLines[0]["y"] == 1
    assert ph_chart.referenceLines == []


def test__create_line_chart_figure__sets_context_line_as_title():
    """GIVEN a context line describing the fixed conditions
    WHEN the download figure is created
    THEN the context line is set as the figure title
    """
    fig = create_line_chart_figure(
        model_results=_fake_results(), par_xaxis=DIC, par_yaxis=PH, lang="de", context_line="Fest: DIC = 1900"
    )

    assert fig.layout.title.text == "Fest: DIC = 1900"
