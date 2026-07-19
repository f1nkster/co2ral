import numpy as np
from core.utils.charts import (
    create_bjerrum_chart,
    create_line_chart,
    create_line_chart_figure,
    create_speciation_chart,
)
from core.utils.marine_model import DIC, OMEGA_ARAGONITE, PCO2, PH, SPECIATION_PARAMS


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


def test__create_line_chart__comparison_adds_second_series():
    """GIVEN a frozen comparison result on the same x grid
    WHEN the line chart is created
    THEN every data row contains both values and a gray comparison series is added
    """
    current = _fake_results()
    frozen = {"par2": current["par2"], "pH": np.linspace(8.2, 7.4, 5)}

    chart = create_line_chart(
        model_results=current,
        par_xaxis=DIC,
        par_yaxis=PH,
        lang="de",
        comparison_results=frozen,
        comparison_suffix=" (Vergleich)",
    )

    assert len(chart.series) == 2
    assert chart.series[1]["name"] == "pH (Vergleich)"
    assert chart.series[1]["color"] == "gray.6"
    assert chart.data[0]["pH (Vergleich)"] == 8.2


def test__create_speciation_chart__stacks_all_three_species_to_percent():
    """GIVEN model results with all three DIC species
    WHEN the speciation chart is created
    THEN it is a 100 % stacked area chart with one series per species
    """
    results = {
        "par2": np.linspace(1800, 2400, 5),
        "CO2": np.linspace(10, 40, 5),
        "HCO3": np.linspace(1600, 2100, 5),
        "CO3": np.linspace(220, 90, 5),
    }

    chart = create_speciation_chart(model_results=results, par_xaxis=DIC, lang="de")

    assert chart.type == "percent"
    assert len(chart.series) == len(SPECIATION_PARAMS)
    assert chart.data[0]["CO₂(aq)"] == 10
    assert chart.data[0]["HCO₃⁻"] == 1600
    assert chart.data[0]["CO₃²⁻"] == 220


def test__create_bjerrum_chart__fractions_pk_markers_and_current_ph():
    """GIVEN model results over a pH range with the three DIC species
    WHEN the Bjerrum chart is created
    THEN the fractions sum to 100 %, pK markers sit at the curve crossings and the
         current pH range is marked
    """
    ph = np.linspace(4, 12, 33)
    # Synthetic but shape-correct speciation: CO2 dominates at low pH, CO3 at high pH.
    co2 = np.linspace(100, 0, 33)
    co3 = np.linspace(0, 100, 33)
    hco3 = 100 - np.abs(co2 - co3) / 2
    results = {"par2": ph, "CO2": co2, "HCO3": hco3, "CO3": co3}

    chart = create_bjerrum_chart(bjerrum_results=results, current_ph_values=np.array([7.8, 8.2]), lang="de")

    assert len(chart.series) == 3
    first_row_sum = sum(v for k, v in chart.data[0].items() if k != "x")
    assert abs(first_row_sum - 100) < 1
    labels = [line.get("label", "") for line in chart.referenceLines]
    assert any("pK₁" in label for label in labels)
    assert any("pK₂" in label for label in labels)
    assert any("aktueller pH" in label for label in labels)
    assert {line["x"] for line in chart.referenceLines if "pK" not in line.get("label", "")} >= {7.8, 8.2}


def test__create_line_chart_figure__sets_context_line_as_title():
    """GIVEN a context line describing the fixed conditions
    WHEN the download figure is created
    THEN the context line is set as the figure title
    """
    fig = create_line_chart_figure(
        model_results=_fake_results(), par_xaxis=DIC, par_yaxis=PH, lang="de", context_line="Fest: DIC = 1900"
    )

    assert fig.layout.title.text == "Fest: DIC = 1900"
