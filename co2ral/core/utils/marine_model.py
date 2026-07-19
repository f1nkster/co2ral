from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import PyCO2SYS
from locales.translation import TRANSLATION_DICT


@dataclass
class MarineModelParameter:
    name: str
    label: dict[str, str]
    unit: str
    type: int = -1
    default_value: float = -1.0
    min_value: float = 0.0
    max_value: float = 100.0

    def get_axis_label(self, lang: str) -> str:
        """Get the axis label of this model parameter.

        :param lang: Language for the label.
        :return: String representing the label.
        """
        return f"{self.label[lang]} [{self.unit}]" if self.unit else f"{self.label[lang]}"

    def get_option(self, lang: str) -> dict:
        """Get the option for this model parameter.

        :param lang: Language for the label.
        :return: Dictionary with value and label.
        """
        return {"value": self.name, "label": self.label[lang]}


@dataclass
class MarineModelParameterCollection:
    name: str
    params: list[MarineModelParameter]

    def get_param_by_name(self, name: str) -> MarineModelParameter | None:
        """Get a parameter by its name.

        :param name: Name of the parameter.
        :return: MarineModelParameter if found, else None.
        """
        for param in self.params:
            if param.name == name:
                return param
        return None

    def get_option_list(self, lang: str) -> list:
        """Get a list of options for the parameters in this collection.

        :param lang: Language for the label.
        :return: List of dictionaries with value and label for each parameter.
        """
        option_list = []
        for param in self.params:
            option_list.append(param.get_option(lang=lang))

        return option_list

    def get_option_list_without_param(self, name: str, lang: str) -> list:
        """Get a list of options for the parameters in this collection, excluding the given parameter.

        :param name: Parameter to exclude.
        :param lang: Language for the label.
        :return: List of dictionaries with value and label for each parameter, excluding the given parameter.
        """
        option_list = []
        for p in self.params:
            if p.name != name:
                option_list.append(p.get_option(lang=lang))

        return option_list


ALKALINITY = MarineModelParameter(
    name="alkalinity",
    label={lang: TRANSLATION_DICT[lang]["total_alkalinity"] for lang in TRANSLATION_DICT},
    type=1,
    default_value=2500,
    unit="μmol/kg",
    min_value=1000,
    max_value=5000,
)
DIC = MarineModelParameter(
    name="dic",
    label={"en": "DIC", "de": "DIC"},
    type=2,
    default_value=1900,
    unit="μmol/kg",
    min_value=0,
    max_value=3000,
)
PH = MarineModelParameter(
    name="pH", label={"en": "pH", "de": "pH"}, type=3, default_value=7, unit="-", min_value=0.0, max_value=14.0
)
PCO2 = MarineModelParameter(
    name="pCO2", label={"en": "pCO₂", "de": "pCO₂"}, type=4, default_value=420, unit="μatm", min_value=0, max_value=1000
)


SYSTEM_PARAMS = MarineModelParameterCollection("Carbonate System Parameters", params=[ALKALINITY, DIC, PH, PCO2])


SALINITY = MarineModelParameter(
    name="salinity",
    label={lang: TRANSLATION_DICT[lang]["practical_salinity"] for lang in TRANSLATION_DICT},
    default_value=30,
    unit="-",
    min_value=0,
    max_value=50,
)
TEMPERATURE = MarineModelParameter(
    name="temperature",
    label={lang: TRANSLATION_DICT[lang]["temperature"] for lang in TRANSLATION_DICT},
    default_value=20,
    unit="°C",
    min_value=-2,
    max_value=30,
)
TOTAL_SILICATE = MarineModelParameter(
    name="total_silicate",
    label={lang: TRANSLATION_DICT[lang]["total_silicate"] for lang in TRANSLATION_DICT},
    default_value=5,
    unit="μmol/kg",
    min_value=0.0,
    max_value=10.0,
)
TOTAL_PHOSPHATE = MarineModelParameter(
    name="total_phosphate",
    label={lang: TRANSLATION_DICT[lang]["total_phosphate"] for lang in TRANSLATION_DICT},
    default_value=1.5,
    unit="μmol/kg",
    min_value=0.0,
    max_value=3.0,
)

CO3 = MarineModelParameter(name="CO3", label={"en": "CO₃²⁻", "de": "CO₃²⁻"}, unit="μmol/kg")
HCO3 = MarineModelParameter(name="HCO3", label={"en": "HCO₃⁻", "de": "HCO₃⁻"}, unit="μmol/kg")

CO2_AQ = MarineModelParameter(name="CO2", label={"en": "CO₂(aq)", "de": "CO₂(aq)"}, unit="μmol/kg")

DIC_PARAMS = MarineModelParameterCollection("DIC Related Parameters", params=[CO2_AQ, HCO3, CO3])

# The three DIC species in the order of the equilibrium cascade CO₂(aq) -> HCO₃⁻ -> CO₃²⁻.
SPECIATION_PARAMS = [CO2_AQ, HCO3, CO3]

# Saturation states straight from the PyCO2SYS results; the names match the result dict keys.
OMEGA_ARAGONITE = MarineModelParameter(
    name="saturation_aragonite", label={"en": "Ω Aragonite", "de": "Ω Aragonit"}, unit="-"
)
OMEGA_CALCITE = MarineModelParameter(name="saturation_calcite", label={"en": "Ω Calcite", "de": "Ω Calcit"}, unit="-")

DERIVED_PARAMS = MarineModelParameterCollection("Derived Parameters", params=[OMEGA_ARAGONITE, OMEGA_CALCITE])

ALL_PARAMS = MarineModelParameterCollection(
    "All Parameters", params=SYSTEM_PARAMS.params + DIC_PARAMS.params + DERIVED_PARAMS.params
)


class MarineModel:
    def __init__(
        self,
        value_par1: float,
        type_par1: int,
        type_par2: int,
        min_value_par2: int,
        max_value_par2: int,
        number_of_steps: int,
        value_salinity: float,
        value_temperature: float,
        value_total_silicate: float,
        value_total_phosphate: float,
    ) -> None:
        self._par1 = value_par1
        self._par1_type = type_par1
        self._par2 = np.linspace(min_value_par2, max_value_par2, number_of_steps)
        self._par2_type = type_par2
        self._salinity = value_salinity
        self._temperature = value_temperature
        self._total_silicate = value_total_silicate
        self._total_phosphate = value_total_phosphate

        # to be adapted to user input
        self._opt_k_carbonic = 4
        self._opt_k_bisulfate = 1
        pass

    def _create_model_args_dict(self) -> dict:
        model_args = {
            "par1": self._par1,  # Value of the first parameter
            "par2": self._par2,  # Value of the second parameter, which is a long vector of different DIC's!
            "par1_type": self._par1_type,  # The first parameter supplied is of type "1", which is "alkalinity"
            "par2_type": self._par2_type,  # The second parameter supplied is of type "2", which is "DIC"
            "salinity": self._salinity,  # Salinity of the sample
            "temperature": self._temperature,  # Temperature at input conditions
            "total_silicate": self._total_silicate,  # Concentration of silicate  in the sample (in umol/kg)
            "total_phosphate": self._total_phosphate,  # Concentration of phosphate in the sample (in umol/kg)
            "opt_k_carbonic": self._opt_k_carbonic,  # Choice of H2CO3 and HCO3- dissociation constants K1 and K2 ("4" means "Mehrbach refit")
            "opt_k_bisulfate": self._opt_k_bisulfate,  # Choice of HSO4- dissociation constants KSO4 ("1" means "Dickson")
        }
        return model_args

    def run(self) -> dict:
        """Runs the marine model with parameter set in the init.

        :return: Result dict.
        """
        model_args = self._create_model_args_dict()

        # Run CO2SYS!
        results = PyCO2SYS.sys(**model_args)

        return results


@lru_cache(maxsize=512)
def run_model_cached(
    value_par1: float,
    type_par1: int,
    type_par2: int,
    min_value_par2: float,
    max_value_par2: float,
    number_of_steps: int,
    value_salinity: float,
    value_temperature: float,
    value_total_silicate: float,
    value_total_phosphate: float,
) -> dict:
    """Runs the marine model with caching. The inputs are discrete slider values, so identical
       parameter combinations recur constantly (especially with live updates and presets) and
       the cache avoids recomputation. Callers must not mutate the returned dict.

    :param value_par1: Value of the first (fixed) parameter.
    :param type_par1: PyCO2SYS type of the first parameter.
    :param type_par2: PyCO2SYS type of the second parameter.
    :param min_value_par2: Minimum value for the second parameter.
    :param max_value_par2: Maximum value for the second parameter.
    :param number_of_steps: Number of steps for the second parameter.
    :param value_salinity: Value for salinity.
    :param value_temperature: Value for temperature.
    :param value_total_silicate: Value for total silicate.
    :param value_total_phosphate: Value for total phosphate.
    :return: Result dict of the model run.
    """
    model = MarineModel(
        value_par1=value_par1,
        type_par1=type_par1,
        type_par2=type_par2,
        min_value_par2=min_value_par2,
        max_value_par2=max_value_par2,
        number_of_steps=number_of_steps,
        value_salinity=value_salinity,
        value_temperature=value_temperature,
        value_total_silicate=value_total_silicate,
        value_total_phosphate=value_total_phosphate,
    )
    return model.run()
