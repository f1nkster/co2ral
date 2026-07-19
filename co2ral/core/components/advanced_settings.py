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


def create_advanced_settings(
    lang: str = "de", settings: Settings | None = None, school_mode: bool = False
) -> dmc.Accordion:
    """Create the advanced settings accordion for the marine model.

    In school mode everything except the temperature slider is hidden: the components stay
    mounted (dash callbacks reference their ids), but students only see the one control that
    is intuitive to explore.

    :param lang: Language for labels, either "de" or "en".
    :param settings: Initial values for all controls; defaults are used if None.
    :param school_mode: Whether to render the reduced school interface.
    :return: The advanced settings accordion component.
    """
    settings = settings or Settings()

    # Get all translations
    dictionary = TRANSLATION_DICT[lang]
    unit = dictionary["unit"]
    content = []
    hidden_class = "school-hidden" if school_mode else None

    x_axis_section = [sel.badge(dictionary["x_axis_settings"])]
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

    x_axis_section.append(x_axis_row)
    content.append(dmc.Box(x_axis_section, className=hidden_class))

    ### Hydrographic Conditions
    content.append(dmc.Box(sel.badge(dictionary["hydrographic_conditions"]), className=hidden_class))
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
    content.append(dmc.Box(salinity_slider, className=hidden_class))
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
    content.append(dmc.Box(sel.badge(dictionary["nutrients"]), className=hidden_class))
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
    content.append(dmc.Box(total_silicate_slider, className=hidden_class))
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
    content.append(dmc.Box(total_phosphate_slider, className=hidden_class))

    # Final assembly the accordion. In school mode the temperature slider is the only control
    # in here, so the section is renamed and opened by default instead of hiding it behind
    # an "advanced settings" label students would not click.
    title = dictionary["school_explore"] if school_mode else dictionary["advanced_settings"]
    accordion = sel.accordion_with_title(
        title,
        dmc.Stack(content, align="stretch", gap="xs"),
        icon="mdi:thermometer" if school_mode else "mdi:database-cog",
        value=title if school_mode else "Controls",
    )

    return accordion
