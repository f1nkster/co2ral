from dataclasses import dataclass

from core.utils.settings import Settings


@dataclass
class Preset:
    """A didactic scenario preset: a named, fully configured settings state."""

    name: str
    label: dict[str, str]
    settings: Settings


PRESETS: list[Preset] = [
    Preset(
        name="acidification",
        label={
            "de": "Ozeanversauerung: pCO₂ 280 → 1000 μatm",
            "en": "Ocean acidification: pCO₂ 280 → 1000 μatm",
        },
        settings=Settings(
            par1_name="alkalinity",
            par1_value=2300,
            par2_name="pCO2",
            par2_min=280,
            par2_max=1000,
            par2_steps=15,
            yaxis_names=["pH", "CO3"],
            salinity=35,
            temperature=18,
        ),
    ),
    Preset(
        name="coral_reef",
        label={
            "de": "Tropisches Korallenriff",
            "en": "Tropical coral reef",
        },
        settings=Settings(
            par1_name="alkalinity",
            par1_value=2350,
            par2_name="pCO2",
            par2_min=280,
            par2_max=800,
            par2_steps=12,
            yaxis_names=["CO3", "pH"],
            salinity=36,
            temperature=28,
        ),
    ),
    Preset(
        name="north_sea",
        label={
            "de": "Nordsee (gemäßigt)",
            "en": "North Sea (temperate)",
        },
        settings=Settings(
            par1_name="alkalinity",
            par1_value=2300,
            par2_name="dic",
            par2_min=1900,
            par2_max=2250,
            par2_steps=12,
            yaxis_names=["pH", "pCO2"],
            salinity=32,
            temperature=10,
        ),
    ),
    Preset(
        name="baltic_sea",
        label={
            "de": "Ostsee (Brackwasser)",
            "en": "Baltic Sea (brackish)",
        },
        settings=Settings(
            par1_name="alkalinity",
            par1_value=1650,
            par2_name="dic",
            par2_min=1400,
            par2_max=1750,
            par2_steps=12,
            yaxis_names=["pH", "pCO2"],
            salinity=8,
            temperature=12,
        ),
    ),
]


def get_preset_options(lang: str) -> list[dict]:
    """Builds the dropdown options for the preset select; the option value is the preset's url query string.

    :param lang: Language for the labels.
    :return: List of dicts with value and label.
    """
    return [{"value": preset.settings.to_query(), "label": preset.label[lang]} for preset in PRESETS]
