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

    def get_axis_label(self) -> str:
        """Get the axis label of this model parameter.

        :return: String representing the label.
        """
        return f"{self.label} [{self.unit}]" if self.unit else f"{self.label}"


ALKALINITY = MarineModelParameter(
    name="alkalinity", label="Total Alkalinity", type=1, default_value=2400, unit="μmol/kg"
)
DIC = MarineModelParameter(name="dic", label="DIC", type=2, default_value=2400, unit="μmol/kg")
PH = MarineModelParameter(name="pH", label="pH", type=3, default_value=7, unit="-")
PCO2 = MarineModelParameter(name="pCO2", label="pCO₂", type=4, default_value=-1, unit="μatm")  # tbd: default value
# PCO2 = ModelParameter(name="pCO2", label="pCO2", type=4, default_value=-1, unit="μatm") # tbd: default value


SALINITY = MarineModelParameter(name="salinity", label="Practical Salinity", default_value=35, unit="-")
TEMPERATURE = MarineModelParameter(name="temperature", label="Temperature", default_value=25, unit="°C")
TOTAL_SILICATE = MarineModelParameter(name="total_silicate", label="Total Silicate", default_value=25, unit="μmol/kg")
TOTAL_PHOSPHATE = MarineModelParameter(
    name="total_phosphate", label="Total Phosphate", default_value=25, unit="μmol/kg"
)

CO3 = MarineModelParameter(name="CO3", label="CO₃", unit="μmol/kg")
HCO3 = MarineModelParameter(name="HCO3", label="HCO₃", unit="μmol/kg")


class MarineModel:
    def __init__(
        self,
        value_par1: float,
        value_salinity: float,
        value_temperature: float,
        value_total_silicate: float,
        value_total_phosphate: float,
    ) -> None:
        self._par1 = value_par1
        self._salinity = value_salinity
        self._temperature = value_temperature
        self._total_silicate = value_total_silicate
        self._total_phosphate = value_total_phosphate

        # to be adapted to user input
        self._par2 = np.arange(2000, 3001, 30)
        self._par1_type = 1
        self._par2_type = 2
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
