from dataclasses import dataclass

import numpy as np
import PyCO2SYS


@dataclass
class MarineModelParameter:
    name: str
    label: str
    unit: str
    type: int = -1
    default_value: float = -1.0
    min_value: float = 0.0
    max_value: float = 100.0

    def get_axis_label(self) -> str:
        """Get the axis label of this model parameter.

        :return: String representing the label.
        """
        return f"{self.label} [{self.unit}]" if self.unit else f"{self.label}"

    def get_option(self) -> dict:
        """Get the option for this model parameter.

        :return: Dictionary with value and label.
        """
        return {"value": self.name, "label": self.label}


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

    def get_option_list(self) -> list:
        """Get a list of options for the parameters in this collection.

        :return: List of dictionaries with value and label for each parameter.
        """
        option_list = []
        for param in self.params:
            option_list.append(param.get_option())

        return option_list

    def get_option_list_without_param(self, name: str | None) -> list:
        """Get a list of options for the parameters in this collection, excluding the given parameter.

        :param name: Parameter to exclude.
        :return: List of dictionaries with value and label for each parameter, excluding the given parameter.
        """
        option_list = []
        for p in self.params:
            if p.name != name:
                option_list.append(p.get_option())

        return option_list


ALKALINITY = MarineModelParameter(
    name="alkalinity",
    label="Total Alkalinity",
    type=1,
    default_value=2500,
    unit="μmol/kg",
    min_value=1000,
    max_value=5000,
)
DIC = MarineModelParameter(
    name="dic", label="DIC", type=2, default_value=1900, unit="μmol/kg", min_value=0, max_value=3000
)
PH = MarineModelParameter(name="pH", label="pH", type=3, default_value=7, unit="-", min_value=0.0, max_value=14.0)
PCO2 = MarineModelParameter(
    name="pCO2", label="pCO₂", type=4, default_value=420, unit="μatm", min_value=0, max_value=1000
)


SYSTEM_PARAMS = MarineModelParameterCollection("Carbonate System Parameters", params=[ALKALINITY, DIC, PH, PCO2])


SALINITY = MarineModelParameter(
    name="salinity", label="Practical Salinity", default_value=30, unit="-", min_value=0, max_value=50
)
TEMPERATURE = MarineModelParameter(
    name="temperature", label="Temperature", default_value=20, unit="°C", min_value=-2, max_value=30
)
TOTAL_SILICATE = MarineModelParameter(
    name="total_silicate", label="Total Silicate", default_value=5, unit="μmol/kg", min_value=0.0, max_value=10.0
)
TOTAL_PHOSPHATE = MarineModelParameter(
    name="total_phosphate", label="Total Phosphate", default_value=1.5, unit="μmol/kg", min_value=0.0, max_value=3.0
)

CO3 = MarineModelParameter(name="CO3", label="CO₃²⁻", unit="μmol/kg")
HCO3 = MarineModelParameter(name="HCO3", label="HCO₃⁻", unit="μmol/kg")

DIC_PARAMS = MarineModelParameterCollection("DIC Related Parameters", params=[CO3, HCO3])

ALL_PARAMS = MarineModelParameterCollection("All Parameters", params=SYSTEM_PARAMS.params + DIC_PARAMS.params)


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
