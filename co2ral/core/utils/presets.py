from dataclasses import dataclass

from core.utils.settings import Settings


@dataclass
class Preset:
    """A didactic scenario preset: a named, fully configured settings state.
    School scenarios additionally carry a guiding question in plain language.
    """

    name: str
    label: dict[str, str]
    settings: Settings
    question: dict[str, str] | None = None


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
            yaxis_names=["pH", "saturation_aragonite"],
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
            yaxis_names=["saturation_aragonite", "pH"],
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


# Everyday scenarios for school use: plain language, one guiding question each,
# all within the range where the model is meaningful.
SCHOOL_PRESETS: list[Preset] = [
    Preset(
        name="ocean_past_future",
        label={
            "de": "Der Ozean: früher, heute, morgen",
            "en": "The ocean: past, present, future",
        },
        question={
            "de": "Was passiert mit dem Meerwasser, wenn immer mehr CO₂ in die Luft gelangt? "
            "Vergleiche 280 μatm (vor der Industrialisierung), 420 μatm (heute) und 1000 μatm (mögliche Zukunft).",
            "en": "What happens to seawater as more and more CO₂ enters the air? "
            "Compare 280 μatm (pre-industrial), 420 μatm (today) and 1000 μatm (a possible future).",
        },
        settings=Settings(
            par1_name="alkalinity",
            par1_value=2300,
            par2_name="pCO2",
            par2_min=280,
            par2_max=1000,
            par2_steps=15,
            yaxis_names=["pH", "saturation_aragonite"],
            salinity=35,
            temperature=18,
        ),
    ),
    Preset(
        name="warm_sea",
        label={
            "de": "Warmes Meer, kaltes Meer",
            "en": "Warm sea, cold sea",
        },
        question={
            "de": "Ziehe am Temperaturregler: Wie viel CO₂ bleibt im Wasser gelöst, wenn es wärmer wird? "
            "Denke an eine Limonade, die in der Sonne steht.",
            "en": "Drag the temperature slider: how much CO₂ stays dissolved as the water warms up? "
            "Think of a soft drink standing in the sun.",
        },
        settings=Settings(
            par1_name="pCO2",
            par1_value=420,
            par2_name="alkalinity",
            par2_min=2000,
            par2_max=2500,
            par2_steps=12,
            yaxis_names=["CO2", "pH"],
            salinity=35,
            temperature=25,
        ),
    ),
    Preset(
        name="corals_at_risk",
        label={
            "de": "Korallen in Gefahr",
            "en": "Corals at risk",
        },
        question={
            "de": "Korallen bauen ihre Skelette aus Kalk. Unterhalb von Ω = 1 (rote Linie) löst sich Kalk auf. "
            "Ab welchem CO₂-Gehalt wird es für die Koralle kritisch?",
            "en": "Corals build their skeletons from calcium carbonate. Below Ω = 1 (red line) it dissolves. "
            "At which CO₂ level does it get critical for the coral?",
        },
        settings=Settings(
            par1_name="alkalinity",
            par1_value=2350,
            par2_name="pCO2",
            par2_min=280,
            par2_max=1000,
            par2_steps=15,
            yaxis_names=["saturation_aragonite"],
            salinity=36,
            temperature=28,
        ),
    ),
    Preset(
        name="baltic_school",
        label={
            "de": "Ostsee: empfindlicher als der Ozean?",
            "en": "Baltic Sea: more sensitive than the ocean?",
        },
        question={
            "de": "Die Ostsee enthält weniger Salz und weniger Kalk als der offene Ozean. "
            "Vergleiche mit dem Ozean-Szenario: Wo sinkt der pH bei gleichem CO₂-Anstieg stärker?",
            "en": "The Baltic Sea contains less salt and less carbonate than the open ocean. "
            "Compare with the ocean scenario: where does pH drop more for the same CO₂ increase?",
        },
        settings=Settings(
            par1_name="alkalinity",
            par1_value=1650,
            par2_name="pCO2",
            par2_min=280,
            par2_max=1000,
            par2_steps=15,
            yaxis_names=["pH"],
            salinity=8,
            temperature=12,
        ),
    ),
]


def get_school_preset_by_name(name: str | None) -> Preset | None:
    """Looks up a school scenario by its name.

    :param name: Scenario name from the url, or None.
    :return: The scenario if found, else None.
    """
    for preset in SCHOOL_PRESETS:
        if preset.name == name:
            return preset
    return None


def get_preset_options(lang: str) -> list[dict]:
    """Builds the dropdown options for the preset select; the option value is the preset's url query string.

    :param lang: Language for the labels.
    :return: List of dicts with value and label.
    """
    return [{"value": preset.settings.to_query(), "label": preset.label[lang]} for preset in PRESETS]
