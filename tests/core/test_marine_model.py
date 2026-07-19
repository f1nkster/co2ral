import numpy as np
from core.utils.marine_model import (
    ALKALINITY,
    ALL_PARAMS,
    DIC,
    SYSTEM_PARAMS,
    MarineModel,
    MarineModelParameter,
    run_model_cached,
)


def test__get_param_by_name__returns_param():
    """GIVEN a parameter collection
    WHEN a contained parameter is requested by name
    THEN the matching parameter object is returned
    """
    assert SYSTEM_PARAMS.get_param_by_name("alkalinity") is ALKALINITY
    assert SYSTEM_PARAMS.get_param_by_name("dic") is DIC


def test__get_param_by_name__returns_none_for_unknown():
    """GIVEN a parameter collection
    WHEN an unknown name is requested
    THEN None is returned
    """
    assert SYSTEM_PARAMS.get_param_by_name("does-not-exist") is None


def test__get_option_list_without_param__excludes_given_param():
    """GIVEN a parameter collection
    WHEN the option list without a specific parameter is requested
    THEN the returned options contain all other parameters but not the excluded one
    """
    options = SYSTEM_PARAMS.get_option_list_without_param("alkalinity", lang="de")

    values = [option["value"] for option in options]
    assert "alkalinity" not in values
    assert len(values) == len(SYSTEM_PARAMS.params) - 1


def test__get_axis_label__with_and_without_unit():
    """GIVEN parameters with and without a unit
    WHEN the axis label is requested
    THEN the unit is appended in brackets only if present
    """
    with_unit = MarineModelParameter(name="x", label={"de": "X"}, unit="μmol/kg")
    without_unit = MarineModelParameter(name="y", label={"de": "Y"}, unit="")

    assert with_unit.get_axis_label(lang="de") == "X [μmol/kg]"
    assert without_unit.get_axis_label(lang="de") == "Y"


def test__all_params__labels_available_in_both_languages():
    """GIVEN all selectable parameters
    WHEN their labels are inspected
    THEN every parameter provides a German and an English label
    """
    for param in ALL_PARAMS.params:
        assert "de" in param.label, f"missing German label for {param.name}"
        assert "en" in param.label, f"missing English label for {param.name}"


def _run_default_model(number_of_steps: int = 10) -> dict:
    """Runs the model with fixed alkalinity over a DIC range under typical seawater conditions.

    :param number_of_steps: Number of steps for the second parameter.
    :return: Result dict of the model run.
    """
    model = MarineModel(
        value_par1=ALKALINITY.default_value,
        type_par1=ALKALINITY.type,
        type_par2=DIC.type,
        min_value_par2=1800,
        max_value_par2=2400,
        number_of_steps=number_of_steps,
        value_salinity=35,
        value_temperature=25,
        value_total_silicate=5,
        value_total_phosphate=1.5,
    )
    return model.run()


def test__marine_model_run__returns_expected_output_shapes():
    """GIVEN a model with a fixed alkalinity and a DIC range
    WHEN the model is run
    THEN the results contain all plottable parameters with one value per step
    """
    number_of_steps = 10
    results = _run_default_model(number_of_steps=number_of_steps)

    for param in ALL_PARAMS.params:
        if param.name == ALKALINITY.name:
            continue
        assert param.name in results, f"missing model output for {param.name}"
        assert len(np.atleast_1d(results[param.name])) == number_of_steps

    assert len(results["par2"]) == number_of_steps


def test__marine_model_run__ph_decreases_with_rising_dic():
    """GIVEN a model with a fixed alkalinity and a rising DIC range
    WHEN the model is run
    THEN pH strictly decreases and pCO2 strictly increases with DIC (ocean acidification)
    """
    results = _run_default_model()

    assert np.all(np.diff(results["pH"]) < 0)
    assert np.all(np.diff(results["pCO2"]) > 0)


def test__marine_model_run__plausible_seawater_values():
    """GIVEN typical present-day surface seawater conditions
    WHEN the model is run
    THEN the resulting pH values lie in a plausible seawater range
    """
    results = _run_default_model()

    assert np.all(results["pH"] > 7.0)
    assert np.all(results["pH"] < 9.0)


def test__run_model_cached__returns_cached_result_for_identical_inputs():
    """GIVEN two identical model parameter sets
    WHEN the cached model runner is called twice
    THEN the second call returns the cached result object without recomputation
    """
    args = (ALKALINITY.default_value, 1, 2, 1800, 2400, 10, 35, 25, 5, 1.5)

    first = run_model_cached(*args)
    second = run_model_cached(*args)

    assert first is second
    assert np.array_equal(first["pH"], MarineModel(*args).run()["pH"])


def test__marine_model_run__saturation_decreases_with_rising_dic():
    """GIVEN a model with a fixed alkalinity and a rising DIC range
    WHEN the model is run
    THEN the aragonite and calcite saturation states strictly decrease (ocean acidification)
    """
    results = _run_default_model()

    assert np.all(np.diff(results["saturation_aragonite"]) < 0)
    assert np.all(np.diff(results["saturation_calcite"]) < 0)
    # Calcite is the more stable mineral, so its saturation is always higher than aragonite's.
    assert np.all(results["saturation_calcite"] > results["saturation_aragonite"])
