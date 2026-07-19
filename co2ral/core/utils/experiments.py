from dataclasses import dataclass

from core.utils.settings import Settings


@dataclass
class Experiment:
    """A guided Le Chatelier experiment: a baseline state and a disturbed state.
    The app loads the disturbed state with the baseline frozen as comparison,
    so the equilibrium response is directly visible.
    """

    name: str
    label: dict[str, str]
    description: dict[str, str]
    baseline: Settings
    disturbed: Settings

    def frozen_conditions(self) -> dict:
        """Returns the baseline conditions in the format of the comparison store.

        :return: Dict for the frozen-store.
        """
        return {
            "par1_name": self.baseline.par1_name,
            "par1_value": self.baseline.par1_value,
            "salinity": self.baseline.salinity,
            "temperature": self.baseline.temperature,
            "total_silicate": self.baseline.total_silicate,
            "total_phosphate": self.baseline.total_phosphate,
        }


EXPERIMENTS: list[Experiment] = [
    Experiment(
        name="co2_increase",
        label={
            "de": "CO₂-Eintrag: pCO₂ 420 → 800 μatm",
            "en": "CO₂ input: pCO₂ 420 → 800 μatm",
        },
        description={
            "de": "Mehr CO₂ in der Atmosphäre löst sich im Wasser. Das Gleichgewicht antwortet auf die "
            "Störung, indem es zusätzliches CO₂ zu HCO₃⁻ und H⁺ umsetzt: Der pH sinkt und die "
            "Karbonat-Sättigung Ω nimmt ab — Ozeanversauerung. Die graue Linie zeigt den Zustand vor der Störung.",
            "en": "More CO₂ in the atmosphere dissolves into the water. The equilibrium responds to the "
            "disturbance by converting additional CO₂ into HCO₃⁻ and H⁺: pH drops and the carbonate "
            "saturation Ω decreases — ocean acidification. The gray line shows the state before the disturbance.",
        },
        baseline=Settings(
            par1_name="pCO2",
            par1_value=420,
            par2_name="alkalinity",
            par2_min=2000,
            par2_max=2500,
            par2_steps=12,
            yaxis_names=["pH", "saturation_aragonite"],
            salinity=35,
            temperature=18,
        ),
        disturbed=Settings(
            par1_name="pCO2",
            par1_value=800,
            par2_name="alkalinity",
            par2_min=2000,
            par2_max=2500,
            par2_steps=12,
            yaxis_names=["pH", "saturation_aragonite"],
            salinity=35,
            temperature=18,
        ),
    ),
    Experiment(
        name="warming",
        label={
            "de": "Erwärmung: 12 → 20 °C",
            "en": "Warming: 12 → 20 °C",
        },
        description={
            "de": "Die Lösung von CO₂ in Wasser ist exotherm — nach Le Chatelier weicht das Gleichgewicht "
            "einer Erwärmung aus: Wärmeres Wasser hält bei gleichem pCO₂ weniger CO₂(aq) in Lösung. "
            "Gleichgewichtskonstanten sind temperaturabhängig. Die graue Linie zeigt das kältere Wasser.",
            "en": "Dissolving CO₂ in water is exothermic — following Le Chatelier, the equilibrium evades "
            "warming: at the same pCO₂, warmer water holds less CO₂(aq) in solution. Equilibrium constants "
            "are temperature dependent. The gray line shows the colder water.",
        },
        baseline=Settings(
            par1_name="pCO2",
            par1_value=420,
            par2_name="alkalinity",
            par2_min=2000,
            par2_max=2500,
            par2_steps=12,
            yaxis_names=["CO2", "pH"],
            salinity=35,
            temperature=12,
        ),
        disturbed=Settings(
            par1_name="pCO2",
            par1_value=420,
            par2_name="alkalinity",
            par2_min=2000,
            par2_max=2500,
            par2_steps=12,
            yaxis_names=["CO2", "pH"],
            salinity=35,
            temperature=20,
        ),
    ),
    Experiment(
        name="alkalinity_increase",
        label={
            "de": "Kalk zugeben: Alkalinität 2100 → 2500 μmol/kg",
            "en": "Add lime: alkalinity 2100 → 2500 μmol/kg",
        },
        description={
            "de": "Verwitterung von Kalkgestein (oder gezielte Zugabe) erhöht die Alkalinität: Das "
            "Puffervermögen steigt, pH und Ω liegen über den gesamten pCO₂-Bereich höher. Genau darauf "
            "beruht die Klimaschutz-Idee 'Ocean Alkalinity Enhancement'. Grau: vor der Zugabe.",
            "en": "Weathering of carbonate rock (or deliberate addition) increases alkalinity: buffering "
            "capacity rises, pH and Ω sit higher across the whole pCO₂ range. This is the basis of the "
            "climate mitigation idea of ocean alkalinity enhancement. Gray: before the addition.",
        },
        baseline=Settings(
            par1_name="alkalinity",
            par1_value=2100,
            par2_name="pCO2",
            par2_min=280,
            par2_max=1000,
            par2_steps=15,
            yaxis_names=["pH", "saturation_aragonite"],
            salinity=35,
            temperature=18,
        ),
        disturbed=Settings(
            par1_name="alkalinity",
            par1_value=2500,
            par2_name="pCO2",
            par2_min=280,
            par2_max=1000,
            par2_steps=15,
            yaxis_names=["pH", "saturation_aragonite"],
            salinity=35,
            temperature=18,
        ),
    ),
    Experiment(
        name="buffer",
        label={
            "de": "Puffer: Meerwasser vs. alkalinitätsarmes Wasser",
            "en": "Buffer: seawater vs. low-alkalinity water",
        },
        description={
            "de": "Gleicher CO₂-Anstieg, unterschiedlicher Puffer: Meerwasser mit hoher Alkalinität (grau) "
            "hält den pH vergleichsweise stabil, alkalinitätsarmes Brackwasser versauert deutlich stärker. "
            "Die Alkalinität wirkt als Puffer gegen Säureeintrag.",
            "en": "Same CO₂ increase, different buffer: seawater with high alkalinity (gray) keeps the pH "
            "comparatively stable, while low-alkalinity brackish water acidifies much more strongly. "
            "Alkalinity acts as a buffer against acid input.",
        },
        baseline=Settings(
            par1_name="alkalinity",
            par1_value=2300,
            par2_name="pCO2",
            par2_min=280,
            par2_max=1000,
            par2_steps=15,
            yaxis_names=["pH"],
            salinity=35,
            temperature=15,
        ),
        disturbed=Settings(
            par1_name="alkalinity",
            par1_value=800,
            par2_name="pCO2",
            par2_min=280,
            par2_max=1000,
            par2_steps=15,
            yaxis_names=["pH"],
            salinity=8,
            temperature=15,
        ),
    ),
]


def get_experiment_by_name(name: str | None) -> Experiment | None:
    """Looks up an experiment by its name.

    :param name: Experiment name from the url, or None.
    :return: The experiment if found, else None.
    """
    for experiment in EXPERIMENTS:
        if experiment.name == name:
            return experiment
    return None
