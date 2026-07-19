import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components import selection as sel
from core.utils.marine_model import (
    SALINITY,
    TEMPERATURE,
    TOTAL_PHOSPHATE,
    TOTAL_SILICATE,
)
from core.utils.settings import Settings
from locales.translation import TRANSLATION_DICT


def create_advanced_settings(lang: str = "de", settings: Settings | None = None) -> dmc.Accordion:
    """Create the advanced settings accordion for the marine model.

    :param lang: Language for labels, either "de" or "en".
    :param settings: Initial values for all controls; defaults are used if None.
    :return: The advanced settings accordion component.
    """
    settings = settings or Settings()

    # Get all translations
    dictionary = TRANSLATION_DICT[lang]
    unit = dictionary["unit"]
    content = []

    content.append(sel.badge(dictionary["x_axis_settings"]))
    x_axis_row = dmc.Stack(
        [
            dmc.NumberInput(
                id="par2-min",
                label=dictionary["x_min_label"],
                value=settings.par2_min,
                min=0,
                step=1,
                debounce=500,
                style={"width": "100%"},
            ),
            dmc.NumberInput(
                id="par2-max",
                label=dictionary["x_max_label"],
                value=settings.par2_max,
                min=0,
                step=1,
                debounce=500,
                style={"width": "100%"},
            ),
            dmc.NumberInput(
                id="par2-steps",
                label=dictionary["num_points"],
                value=settings.par2_steps,
                min=1,
                step=1,
                max=25,
                debounce=500,
                style={"width": "100%"},
            ),
        ],
        gap="xs",
    )

    content.append(x_axis_row)

    ### Hydrographic Conditions
    content.append(sel.badge(dictionary["hydrographic_conditions"]))
    salinity_slider = sel.range_slider(
        id="slider-salinity",
        name=dictionary["practical_salinity"],
        sub_text=f"{unit}: {SALINITY.unit}",
        value=settings.salinity,
        min_val=SALINITY.min_value,
        max_val=SALINITY.max_value,
        step=1,
        info=dictionary.get("expl_salinity"),
    )
    content.append(salinity_slider)
    content.append(dbc.Row(style={"height": "10px"}))
    temperature_slider = sel.range_slider(
        id="slider-temperature",
        name=dictionary["temperature"],
        sub_text=f"{unit}: {TEMPERATURE.unit}",
        value=settings.temperature,
        min_val=TEMPERATURE.min_value,
        max_val=TEMPERATURE.max_value,
        step=1,
        info=dictionary.get("expl_temperature"),
    )
    content.append(temperature_slider)
    content.append(dbc.Row(style={"height": "40px"}))

    ### Nutrients
    content.append(sel.badge(dictionary["nutrients"]))
    total_silicate_slider = sel.range_slider(
        id="slider-total-silicate",
        name=dictionary["total_silicate"],
        sub_text=f"{unit}: μmol/kg",
        value=settings.total_silicate,
        min_val=TOTAL_SILICATE.min_value,
        max_val=TOTAL_SILICATE.max_value,
        step=1,
        info=dictionary.get("expl_total_silicate"),
    )
    content.append(total_silicate_slider)
    content.append(dbc.Row(style={"height": "10px"}))
    total_phosphate_slider = sel.range_slider(
        id="slider-total_phosphate",
        name=dictionary["total_phosphate"],
        sub_text=f"{unit}: μmol/kg",
        value=settings.total_phosphate,
        min_val=TOTAL_PHOSPHATE.min_value,
        max_val=TOTAL_PHOSPHATE.max_value,
        step=1,
        info=dictionary.get("expl_total_phosphate"),
    )
    content.append(total_phosphate_slider)

    # Final assembly the accordion
    accordion = sel.accordion_with_title(
        dictionary["advanced_settings"], dmc.Stack(content, align="stretch", gap="xs"), icon="mdi:database-cog"
    )

    return accordion
