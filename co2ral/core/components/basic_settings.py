import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components import selection as sel
from core.utils.marine_model import (
    DIC_PARAMS,
    SYSTEM_PARAMS,
)
from dash import html
from env.colors import DMC_LIME, DMC_RED
from locales.translation import TRANSLATION_DICT


def create_basic_settings(lang: str = "de") -> dmc.Accordion:
    """Create the basic settings accordion for the marine model.

    :param lang: Language for labels, either "de" or "en".
    :return: The basic settings accordion component.
    """
    # Get all translations and option lists
    dictionary = TRANSLATION_DICT[lang]
    fixed_param_data = SYSTEM_PARAMS.get_option_list(lang=lang)
    y_axis_params = fixed_param_data + DIC_PARAMS.get_option_list(lang=lang)
    accordion_title = TRANSLATION_DICT[lang]["basic_settings"]
    content = []

    # Model settings
    content.append(sel.badge(dictionary["model_settings"]))
    content.append(
        sel.dropdown_with_title(
            dictionary["fixed_parameter"],
            id="par1-dd",
            description=dictionary["fixed_parameter_description"],
            data=fixed_param_data,
        )
    )
    content.append(html.Div("", id="slider-par1-container"))
    content.append(dbc.Row(style={"height": "30px"}))

    # Plot settings
    content.append(sel.badge(dictionary["plot_settings"]))
    content.append(
        sel.dropdown_with_title(
            dictionary["x_axis_parameter"], id="par2-dd", description=dictionary["x_axis_parameter_description"]
        )
    )
    content.append(
        dmc.MultiSelect(
            label=dictionary["y_axis_parameter"],
            description=dictionary["y_axis_parameter_description"],
            id="yaxis-multiselect",
            data=y_axis_params,
            value=[],
            maxValues=5,
            searchable=True,
            clearable=True,
            style={"width": "100%"},
        )
    )
    content.append(dbc.Row(style={"height": "30px"}))

    #  Apply and Reset Buttons
    reset_button = sel.button(
        "reset-btn",
        dictionary["reset_btn"],
        "ix:reset",
        color=DMC_RED,
    )
    apply_button = sel.button(
        "apply-btn",
        dictionary["apply_btn"],
        "ph:play-duotone",
        color=DMC_LIME,
    )
    buttons = dmc.Stack(
        [
            dbc.Row(
                [
                    dbc.Col(reset_button, width=6),
                    dbc.Col(apply_button, width=6),
                ]
            ),
        ]
    )
    content.append(buttons)

    # Final assembly the accordion
    accordion = sel.accordion_with_title(
        accordion_title, dmc.Stack(content, align="stretch", gap="xs"), icon="mdi:cog-outline", value=accordion_title
    )

    return accordion
