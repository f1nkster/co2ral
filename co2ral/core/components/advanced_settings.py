import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components import selection as sel
from core.utils.marine_model import (
    TOTAL_PHOSPHATE,
    TOTAL_SILICATE,
)
from locales.translation import TRANSLATION_DICT


def create_advanced_settings(lang: str = "de") -> dmc.Accordion:
    """Create the advanced settings accordion for the marine model.

    :param lang: Language for labels, either "de" or "en".
    :return: The advanced settings accordion component.
    """
    # Get all translations
    dictionary = TRANSLATION_DICT[lang]
    unit = TRANSLATION_DICT[lang]["unit"]
    content = []

    content.append(sel.badge(dictionary["x_axis_settings"]))
    x_axis_row = dmc.Stack(
        [
            dmc.NumberInput(
                id="par2-min",
                label=dictionary["x_min_label"],
                min=0,
                step=1,
                style={"width": "100%"},
            ),
            dmc.NumberInput(
                id="par2-max",
                label=dictionary["x_max_label"],
                min=0,
                step=1,
                style={"width": "100%"},
            ),
            dmc.NumberInput(
                id="par2-steps",
                label=dictionary["num_points"],
                value=10,
                min=1,
                step=1,
                max=25,
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
        sub_text=f"{unit}: -",
        value=35,
        min_val=10,
        max_val=50,
        step=1,
    )
    content.append(salinity_slider)
    content.append(dbc.Row(style={"height": "10px"}))
    temperature_slider = sel.range_slider(
        id="slider-temperature",
        name=dictionary["temperature"],
        sub_text=f"{unit}: °C",
        value=25,
        min_val=5,
        max_val=40,
        step=1,
    )
    content.append(temperature_slider)
    content.append(dbc.Row(style={"height": "40px"}))

    ### Nutrients
    content.append(sel.badge(dictionary["nutrients"]))
    total_silicate_slider = sel.range_slider(
        id="slider-total-silicate",
        name=dictionary["total_silicate"],
        sub_text=f"{unit}: μmol/kg",
        value=TOTAL_SILICATE.default_value,
        min_val=TOTAL_SILICATE.min_value,
        max_val=TOTAL_SILICATE.max_value,
        step=1,
    )
    content.append(total_silicate_slider)
    content.append(dbc.Row(style={"height": "10px"}))
    total_phosphate_slider = sel.range_slider(
        id="slider-total_phosphate",
        name=dictionary["total_phosphate"],
        sub_text=f"{unit}: μmol/kg",
        value=TOTAL_PHOSPHATE.default_value,
        min_val=TOTAL_PHOSPHATE.min_value,
        max_val=TOTAL_PHOSPHATE.max_value,
        step=1,
    )
    content.append(total_phosphate_slider)

    # Final assembly the accordion
    accordion = sel.accordion_with_title(
        dictionary["advanced_settings"], dmc.Stack(content, align="stretch", gap="xs"), icon="mdi:database-cog"
    )

    return accordion
