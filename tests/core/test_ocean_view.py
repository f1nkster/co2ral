from core.utils.marine_model import run_single_state
from core.utils.ocean_view import (
    _DELTA_COLORS,
    PCO2_MILESTONES,
    _delta_text,
    _format_number,
    create_ocean_view,
)


def _collect_text(component) -> str:
    """Collects all text contained in a dash component tree.

    :param component: Component or primitive to walk.
    :return: Concatenated text of the whole tree.
    """
    if component is None:
        return ""
    if isinstance(component, str | int | float):
        return str(component)
    if isinstance(component, list | tuple):
        return " ".join(_collect_text(item) for item in component)

    text = ""
    for attribute in ("children", "label", "title"):
        if hasattr(component, attribute):
            text += " " + _collect_text(getattr(component, attribute))
    return text


def test__run_single_state__returns_plausible_present_day_values():
    """GIVEN today's CO2 level and typical surface conditions
    WHEN the single state is computed
    THEN pH and the saturation states lie in the expected present-day ranges
    """
    state = run_single_state(value_pco2=420, value_temperature=18)

    assert 7.9 < state["pH"] < 8.2
    assert 2.0 < state["saturation_aragonite"] < 4.0
    assert state["saturation_calcite"] > state["saturation_aragonite"]
    assert state["HCO3"] > state["CO3"] > state["CO2"]


def test__run_single_state__more_co2_lowers_ph_and_saturation():
    """GIVEN two CO2 levels at the same temperature
    WHEN both states are computed
    THEN the higher CO2 level has a lower pH and a lower aragonite saturation
    """
    preindustrial = run_single_state(value_pco2=280, value_temperature=18)
    future = run_single_state(value_pco2=936, value_temperature=18)

    assert future["pH"] < preindustrial["pH"]
    assert future["saturation_aragonite"] < preindustrial["saturation_aragonite"]
    assert future["CO2"] > preindustrial["CO2"]


def test__format_number__uses_decimal_comma_in_german():
    """GIVEN a value with decimals
    WHEN it is formatted for both languages
    THEN German uses a comma and English a dot
    """
    assert _format_number(8.052, 2, "de") == "8,05"
    assert _format_number(8.052, 2, "en") == "8.05"


def test__delta_text__direction_and_neutral_case():
    """GIVEN values above, below and equal to the reference
    WHEN the change indicator is built
    THEN it points in the right direction and marks negligible changes as unchanged
    """
    down_text, down_color = _delta_text(7.9, 8.2, 2, "de")
    up_text, up_color = _delta_text(8.4, 8.2, 2, "de")
    equal_text, _ = _delta_text(8.2, 8.2, 2, "de")

    assert down_text.startswith("▼") and "0,30" in down_text
    assert down_color == _DELTA_COLORS["down"]
    assert up_text.startswith("▲")
    assert up_color == _DELTA_COLORS["up"]
    assert equal_text == "±0"


def test__create_ocean_view__shows_values_and_coral_verdict():
    """GIVEN a present-day ocean state
    WHEN the picture is built
    THEN it contains the CO2 level, the labels of the water values and a coral verdict
    """
    view = create_ocean_view(value_pco2=420, value_temperature=18, lang="de")
    text = _collect_text(view)

    assert "420" in text
    assert "Säuregrad (pH)" in text
    assert "Kalk-Sättigung" in text
    assert "Korallen" in text or "Kalk löst sich auf" in text


def test__create_ocean_view__coral_verdict_turns_critical_at_high_co2():
    """GIVEN a very high CO2 level
    WHEN the picture is built
    THEN the verdict warns that building calcium carbonate gets harder or impossible
    """
    text = _collect_text(create_ocean_view(value_pco2=1200, value_temperature=28, lang="de"))

    assert "schwieriger" in text or "löst sich auf" in text


def test__pco2_milestones__have_translation_keys_and_rising_values():
    """GIVEN the milestone shortcuts
    WHEN their values are inspected
    THEN they rise from pre-industrial to the future scenario
    """
    values = list(PCO2_MILESTONES.values())

    assert values == sorted(values)
    assert values[0] == 280
