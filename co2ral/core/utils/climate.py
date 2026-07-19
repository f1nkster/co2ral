"""Optional coupling of water temperature to the CO2 level.

The carbonate model itself has no causal link from CO2 to temperature — that link runs
through the greenhouse effect, which is a climate model and not part of PyCO2SYS. The
coupling here is therefore an assumption bolted on top, switched off by default, and it is
named in the interface whenever it is active.

The two constants below are illustrative placeholders chosen so that today's level lands
near the observed sea surface temperature. They are not derived from a cited source and
should be replaced with values confirmed by the chair before the tool is used to make any
statement about future climate.
"""

import math

from core.utils.ocean_view import PREINDUSTRIAL_PCO2


# --- Assumption, to be confirmed --------------------------------------------------------
# Sea surface warming per doubling of atmospheric CO2. Smaller than the equilibrium climate
# sensitivity, because the sea surface warms less and slower than the global mean.
SEA_SURFACE_WARMING_PER_DOUBLING = 1.5

# Sea surface temperature at the pre-industrial CO2 level, in °C.
PREINDUSTRIAL_SEA_SURFACE_TEMPERATURE = 17.1
# ----------------------------------------------------------------------------------------


def coupled_temperature(value_pco2: float, minimum: float = 0, maximum: float = 32) -> int:
    """Water temperature belonging to a CO2 level under the coupling assumption.

    The warming grows with the logarithm of the CO2 level, mirroring how radiative forcing
    scales — not linearly with the concentration.

    :param value_pco2: CO2 partial pressure in the air, in μatm.
    :param minimum: Lower bound of the temperature slider.
    :param maximum: Upper bound of the temperature slider.
    :return: Temperature in °C, rounded to the slider step and clamped to its range.
    """
    doublings = math.log(max(value_pco2, 1.0) / PREINDUSTRIAL_PCO2) / math.log(2)
    temperature = PREINDUSTRIAL_SEA_SURFACE_TEMPERATURE + SEA_SURFACE_WARMING_PER_DOUBLING * doublings
    return int(min(max(round(temperature), minimum), maximum))
