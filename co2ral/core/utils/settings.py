from dataclasses import dataclass, field
from typing import Any

from core.utils.marine_model import (
    ALKALINITY,
    ALL_PARAMS,
    DIC,
    PH,
    SALINITY,
    SYSTEM_PARAMS,
    TEMPERATURE,
    TOTAL_PHOSPHATE,
    TOTAL_SILICATE,
)


def _to_float(value: Any, fallback: float) -> float:
    """Parses a value to float, returning the fallback on invalid input.

    :param value: Raw value, e.g. from a url query.
    :param fallback: Value to use if parsing fails.
    :return: Parsed float or fallback.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _to_int(value: Any, fallback: int) -> int:
    """Parses a value to int, returning the fallback on invalid input.

    :param value: Raw value, e.g. from a url query.
    :param fallback: Value to use if parsing fails.
    :return: Parsed int or fallback.
    """
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return fallback


def _format_number(value: float) -> str:
    """Formats a number for a url query without a trailing .0 for integers.

    :param value: Number to format.
    :return: Compact string representation.
    """
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:g}"


@dataclass
class Settings:
    """All user-adjustable state of the marine model UI, mappable to and from url query parameters."""

    par1_name: str = ALKALINITY.name
    par1_value: float = ALKALINITY.default_value
    par2_name: str = DIC.name
    par2_min: float = DIC.min_value
    par2_max: float = DIC.max_value
    par2_steps: int = 10
    yaxis_names: list[str] = field(default_factory=lambda: [PH.name])
    salinity: float = SALINITY.default_value
    temperature: float = TEMPERATURE.default_value
    total_silicate: float = TOTAL_SILICATE.default_value
    total_phosphate: float = TOTAL_PHOSPHATE.default_value

    @classmethod
    def from_query(cls, url_queries: dict) -> "Settings":
        """Builds settings from url query parameters, falling back to defaults for missing or invalid values.

        :param url_queries: Query parameters, e.g. {"par1": "alkalinity", "par1val": "2300", "y": "pH,CO3"}.
        :return: Validated settings.
        """
        defaults = cls()

        par1 = SYSTEM_PARAMS.get_param_by_name(str(url_queries.get("par1", defaults.par1_name)))
        if par1 is None:
            par1 = ALKALINITY

        par2 = SYSTEM_PARAMS.get_param_by_name(str(url_queries.get("par2", defaults.par2_name)))
        if par2 is None or par2.name == par1.name:
            par2 = next(p for p in SYSTEM_PARAMS.params if p.name != par1.name)

        yaxis_raw = str(url_queries["y"]).split(",") if url_queries.get("y") else list(defaults.yaxis_names)
        yaxis_names = [n for n in yaxis_raw if ALL_PARAMS.get_param_by_name(n) is not None and n != par2.name]
        if not yaxis_names:
            yaxis_names = [next(p.name for p in ALL_PARAMS.params if p.name != par2.name)]

        return cls(
            par1_name=par1.name,
            par1_value=_to_float(url_queries.get("par1val"), par1.default_value),
            par2_name=par2.name,
            par2_min=_to_float(url_queries.get("min"), par2.min_value),
            par2_max=_to_float(url_queries.get("max"), par2.max_value),
            par2_steps=_to_int(url_queries.get("steps"), defaults.par2_steps),
            yaxis_names=yaxis_names,
            salinity=_to_float(url_queries.get("sal"), defaults.salinity),
            temperature=_to_float(url_queries.get("temp"), defaults.temperature),
            total_silicate=_to_float(url_queries.get("sil"), defaults.total_silicate),
            total_phosphate=_to_float(url_queries.get("phos"), defaults.total_phosphate),
        )

    def to_query(self) -> str:
        """Serializes the settings to a url query string (without leading ? and without lang).

        :return: Query string, e.g. "par1=alkalinity&par1val=2300&...".
        """
        return (
            f"par1={self.par1_name}"
            f"&par1val={_format_number(self.par1_value)}"
            f"&par2={self.par2_name}"
            f"&min={_format_number(self.par2_min)}"
            f"&max={_format_number(self.par2_max)}"
            f"&steps={self.par2_steps}"
            f"&y={','.join(self.yaxis_names)}"
            f"&sal={_format_number(self.salinity)}"
            f"&temp={_format_number(self.temperature)}"
            f"&sil={_format_number(self.total_silicate)}"
            f"&phos={_format_number(self.total_phosphate)}"
        )
