import urllib.parse

from core.utils.experiments import EXPERIMENTS, get_experiment_by_name
from core.utils.presets import PRESETS, SCHOOL_PRESETS, get_preset_options, get_school_preset_by_name
from core.utils.settings import Settings


def _parse(query: str) -> dict:
    """Parses a query string into a dict, as dash passes url parameters to the page layout.

    :param query: Query string without leading ?.
    :return: Dict of query parameters.
    """
    return dict(urllib.parse.parse_qsl(query))


def test__settings__default_roundtrip():
    """GIVEN default settings
    WHEN they are serialized to a query string and parsed back
    THEN the resulting settings are identical
    """
    settings = Settings()

    assert Settings.from_query(_parse(settings.to_query())) == settings


def test__settings__from_query_with_valid_values():
    """GIVEN a query with valid custom values
    WHEN settings are parsed from it
    THEN all values are applied
    """
    query = "par1=pCO2&par1val=420&par2=alkalinity&min=1500&max=3000&steps=15&y=pH,CO3&sal=35&temp=25&sil=2&phos=0.5"

    settings = Settings.from_query(_parse(query))

    assert settings.par1_name == "pCO2"
    assert settings.par1_value == 420
    assert settings.par2_name == "alkalinity"
    assert settings.par2_min == 1500
    assert settings.par2_max == 3000
    assert settings.par2_steps == 15
    assert settings.yaxis_names == ["pH", "CO3"]
    assert settings.salinity == 35
    assert settings.temperature == 25
    assert settings.total_silicate == 2
    assert settings.total_phosphate == 0.5


def test__settings__from_query_with_garbage_falls_back_to_defaults():
    """GIVEN a query with invalid parameter names and non-numeric values
    WHEN settings are parsed from it
    THEN the defaults are used instead of crashing
    """
    query = "par1=unknown&par1val=abc&par2=nope&min=x&max=y&steps=z&y=alsounknown&sal=&temp=None"

    settings = Settings.from_query(_parse(query))
    defaults = Settings()

    assert settings.par1_name == defaults.par1_name
    assert settings.par1_value == defaults.par1_value
    assert settings.par2_name == defaults.par2_name
    assert settings.par2_steps == defaults.par2_steps
    assert settings.salinity == defaults.salinity
    assert settings.temperature == defaults.temperature
    assert len(settings.yaxis_names) > 0


def test__settings__par2_never_equals_par1():
    """GIVEN a query where both parameters are the same
    WHEN settings are parsed from it
    THEN the second parameter is switched to a different one
    """
    settings = Settings.from_query(_parse("par1=dic&par2=dic"))

    assert settings.par1_name == "dic"
    assert settings.par2_name != "dic"


def test__settings__yaxis_never_contains_par2():
    """GIVEN a query where a y-axis parameter equals the x-axis parameter
    WHEN settings are parsed from it
    THEN the colliding parameter is removed from the y-axis selection
    """
    settings = Settings.from_query(_parse("par2=pH&y=pH,pCO2"))

    assert settings.yaxis_names == ["pCO2"]


def test__settings__to_query_formats_integers_without_decimal():
    """GIVEN settings with integral float values
    WHEN they are serialized to a query string
    THEN the numbers contain no trailing .0
    """
    query = Settings(par1_value=2300.0, total_phosphate=1.5).to_query()

    assert "par1val=2300" in query
    assert "par1val=2300.0" not in query
    assert "phos=1.5" in query


def test__settings__bjerrum_flag_roundtrip():
    """GIVEN settings with the Bjerrum plot enabled
    WHEN they are serialized and parsed back
    THEN the flag survives, and it defaults to off without the query parameter
    """
    enabled = Settings(show_bjerrum=True)

    assert "bjerrum=1" in enabled.to_query()
    assert Settings.from_query(_parse(enabled.to_query())).show_bjerrum is True
    assert Settings.from_query({}).show_bjerrum is False


def test__experiments__disturbed_settings_roundtrip_and_labels():
    """GIVEN all defined experiments
    WHEN their disturbed settings are serialized and parsed back
    THEN they survive unchanged, and every experiment provides labels, descriptions
         and frozen baseline conditions in both languages
    """
    for experiment in EXPERIMENTS:
        parsed = Settings.from_query(_parse(experiment.disturbed.to_query()))
        assert parsed == experiment.disturbed, f"experiment {experiment.name} does not survive the url roundtrip"

        for lang in ("de", "en"):
            assert experiment.label[lang]
            assert experiment.description[lang]

        frozen = experiment.frozen_conditions()
        assert frozen["par1_name"] == experiment.baseline.par1_name
        assert frozen["salinity"] == experiment.baseline.salinity
        # The disturbance must actually change at least one frozen condition,
        # otherwise the comparison would show two identical curves.
        disturbed_conditions = {
            "par1_name": experiment.disturbed.par1_name,
            "par1_value": experiment.disturbed.par1_value,
            "salinity": experiment.disturbed.salinity,
            "temperature": experiment.disturbed.temperature,
            "total_silicate": experiment.disturbed.total_silicate,
            "total_phosphate": experiment.disturbed.total_phosphate,
        }
        assert disturbed_conditions != frozen, f"experiment {experiment.name} does not disturb anything"


def test__get_experiment_by_name__lookup():
    """GIVEN the experiment registry
    WHEN experiments are looked up by name
    THEN known names resolve and unknown names return None
    """
    assert get_experiment_by_name("co2_increase") is EXPERIMENTS[0]
    assert get_experiment_by_name("does-not-exist") is None
    assert get_experiment_by_name(None) is None


def test__presets__roundtrip_through_query():
    """GIVEN all defined presets
    WHEN their settings are serialized to a query and parsed back
    THEN the settings survive unchanged (i.e. every preset is a valid share url)
    """
    for preset in PRESETS:
        parsed = Settings.from_query(_parse(preset.settings.to_query()))
        assert parsed == preset.settings, f"preset {preset.name} does not survive the url roundtrip"


def test__school_presets__roundtrip_labels_and_questions():
    """GIVEN all school scenarios
    WHEN their settings are serialized and parsed back
    THEN they survive unchanged and every scenario has a label and a guiding question
         in both languages
    """
    for preset in SCHOOL_PRESETS:
        parsed = Settings.from_query(_parse(preset.settings.to_query()))
        assert parsed == preset.settings, f"school scenario {preset.name} does not survive the url roundtrip"

        assert preset.question is not None, f"school scenario {preset.name} has no guiding question"
        for lang in ("de", "en"):
            assert preset.label[lang]
            assert preset.question[lang]


def test__get_school_preset_by_name__lookup():
    """GIVEN the school scenario registry
    WHEN scenarios are looked up by name
    THEN known names resolve and unknown names return None
    """
    assert get_school_preset_by_name("ocean_past_future") is SCHOOL_PRESETS[0]
    assert get_school_preset_by_name("does-not-exist") is None
    assert get_school_preset_by_name(None) is None


def test__presets__provide_labels_in_both_languages():
    """GIVEN all defined presets
    WHEN the dropdown options are built for both languages
    THEN every preset has a label and a non-empty query value
    """
    for lang in ("de", "en"):
        options = get_preset_options(lang)
        assert len(options) == len(PRESETS)
        for option in options:
            assert option["label"]
            assert "par1=" in option["value"]
