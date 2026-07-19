from core.utils.climate import (
    PREINDUSTRIAL_SEA_SURFACE_TEMPERATURE,
    SEA_SURFACE_WARMING_PER_DOUBLING,
    coupled_temperature,
)
from core.utils.marine_model import run_single_state
from core.utils.ocean_view import PREINDUSTRIAL_PCO2


def test__coupled_temperature__starts_at_the_preindustrial_baseline():
    """GIVEN the pre-industrial CO2 level
    WHEN the coupled temperature is derived
    THEN it equals the assumed pre-industrial sea surface temperature
    """
    assert coupled_temperature(PREINDUSTRIAL_PCO2) == round(PREINDUSTRIAL_SEA_SURFACE_TEMPERATURE)


def test__coupled_temperature__adds_one_step_per_doubling():
    """GIVEN a doubling of the CO2 level
    WHEN the coupled temperature is derived
    THEN it rises by the assumed warming per doubling
    """
    baseline = PREINDUSTRIAL_SEA_SURFACE_TEMPERATURE
    doubled = coupled_temperature(PREINDUSTRIAL_PCO2 * 2)

    assert doubled == round(baseline + SEA_SURFACE_WARMING_PER_DOUBLING)


def test__coupled_temperature__grows_logarithmically_not_linearly():
    """GIVEN one and two doublings of the CO2 level
    WHEN the coupled temperatures are derived
    THEN two doublings warm about twice as much as one, not four times as a relation
         linear in the concentration would give
    """
    one_doubling = coupled_temperature(560) - coupled_temperature(280)
    two_doublings = coupled_temperature(1120) - coupled_temperature(280)

    # The tolerance covers the rounding to whole degrees of the slider step.
    assert abs(two_doublings - 2 * one_doubling) <= 1
    assert two_doublings < 4 * one_doubling


def test__coupled_temperature__stays_within_the_slider_range():
    """GIVEN extreme CO2 levels
    WHEN the coupled temperature is derived
    THEN it never leaves the range of the temperature slider
    """
    for value_pco2 in (1, 280, 5000):
        assert 0 <= coupled_temperature(value_pco2, minimum=0, maximum=32) <= 32


def test__climate_coupling__softens_the_saturation_decline():
    """GIVEN a CO2 rise with and without the coupled warming
    WHEN both states are computed
    THEN the warming raises the aragonite saturation slightly while the pH stays put,
         which is exactly the non-obvious effect the coupling is meant to show
    """
    without_warming = run_single_state(value_pco2=936, value_temperature=coupled_temperature(420))
    with_warming = run_single_state(value_pco2=936, value_temperature=coupled_temperature(936))

    assert with_warming["saturation_aragonite"] > without_warming["saturation_aragonite"]
    assert abs(with_warming["pH"] - without_warming["pH"]) < 0.02
