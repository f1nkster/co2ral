import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components import selection as sel
from core.utils.experiments import EXPERIMENTS
from core.utils.marine_model import (
    ALL_PARAMS,
    SYSTEM_PARAMS,
    MarineModelParameter,
)
from core.utils.presets import SCHOOL_PRESETS, get_preset_options
from core.utils.settings import Settings
from dash import dcc, html
from dash_iconify import DashIconify
from env.colors import DMC_GRAY, DMC_LIME, DMC_RED, DMC_TEAL
from locales.translation import TRANSLATION_DICT


def create_par1_slider(param: MarineModelParameter, value: float, lang: str) -> dmc.Slider:
    """Creates the value slider for the fixed parameter.

    :param param: The fixed parameter.
    :param value: Initial slider value.
    :param lang: Language for labels.
    :return: Slider component with title, unit line and info tooltip.
    """
    unit = TRANSLATION_DICT[lang]["unit"]
    step = 10 if param.unit == "μmol/kg" else 1

    return sel.range_slider(
        id="slider-par1",
        name=param.label[lang],
        sub_text=f"{unit}: {param.unit}",
        value=value,
        min_val=param.min_value,
        max_val=param.max_value,
        step=step,
        info=TRANSLATION_DICT[lang].get(f"expl_{param.name}"),
    )


def create_school_scenarios(lang: str) -> list:
    """Creates the everyday scenario buttons shown in school mode.

    :param lang: Language for labels.
    :return: List of components: heading, intro text and one link button per scenario.
    """
    dictionary = TRANSLATION_DICT[lang]
    components = [
        sel.badge(dictionary["school_scenarios"]),
        dmc.Text(dictionary["school_intro"], size="xs", c="dimmed", mb=4),
    ]
    for preset in SCHOOL_PRESETS:
        components.append(
            html.A(
                dmc.Button(
                    preset.label[lang],
                    variant="light",
                    size="md",
                    color=DMC_TEAL,
                    fullWidth=True,
                    styles={"label": {"whiteSpace": "normal", "textAlign": "left"}},
                    leftSection=DashIconify(icon="mdi:earth", width=20),
                ),
                href=f"/?{preset.settings.to_query()}&scen={preset.name}&mode=schule&lang={lang}",
                style={"textDecoration": "none"},
            )
        )
    components.append(dbc.Row(style={"height": "10px"}))
    return components


def create_basic_settings(
    lang: str = "de",
    settings: Settings | None = None,
    comparison_active: bool = False,
    school_mode: bool = False,
) -> dmc.Accordion:
    """Create the basic settings accordion for the marine model.

    In school mode the technical controls stay mounted (all dash callbacks reference their ids)
    but are hidden, so only the everyday scenarios and a few explorable controls remain visible.

    :param lang: Language for labels, either "de" or "en".
    :param settings: Initial values for all controls; defaults are used if None.
    :param comparison_active: Whether the comparison mode starts active (e.g. in an experiment).
    :param school_mode: Whether to render the reduced school interface.
    :return: The basic settings accordion component.
    """
    settings = settings or Settings()

    # Get all translations and option lists
    dictionary = TRANSLATION_DICT[lang]
    fixed_param_data = SYSTEM_PARAMS.get_option_list(lang=lang)
    y_axis_params = ALL_PARAMS.get_option_list_without_param(settings.par2_name, lang=lang)
    accordion_title = dictionary["basic_settings"]
    par1 = SYSTEM_PARAMS.get_param_by_name(settings.par1_name)
    content = []

    if school_mode:
        content.extend(create_school_scenarios(lang=lang))

    # Everything from here to the plot settings is technical detail, hidden in school mode.
    technical = []

    # Scenario presets
    technical.append(sel.badge(dictionary["scenarios"]))
    technical.append(
        dmc.Select(
            id="preset-dd",
            data=get_preset_options(lang),
            placeholder=dictionary["scenario_placeholder"],
            clearable=True,
            searchable=False,
            style={"width": "100%"},
        )
    )
    technical.append(dbc.Row(style={"height": "10px"}))

    # Guided Le Chatelier experiments: links that load a disturbed state with the
    # baseline frozen as comparison.
    technical.append(sel.badge(dictionary["experiments"]))
    technical.append(dmc.Text(dictionary["experiments_hint"], size="xs", c="dimmed"))
    for experiment in EXPERIMENTS:
        technical.append(
            html.A(
                dmc.Button(
                    experiment.label[lang],
                    variant="light",
                    size="compact-sm",
                    color=DMC_TEAL,
                    fullWidth=True,
                    styles={"label": {"whiteSpace": "normal", "textAlign": "left"}},
                    leftSection=DashIconify(icon="mdi:flask-outline", width=16),
                ),
                href=f"/?{experiment.disturbed.to_query()}&exp={experiment.name}&lang={lang}",
                style={"textDecoration": "none"},
            )
        )
    technical.append(dbc.Row(style={"height": "10px"}))

    # Model settings
    technical.append(sel.badge(dictionary["model_settings"]))
    technical.append(
        sel.dropdown_with_title(
            dictionary["fixed_parameter"],
            id="par1-dd",
            description=dictionary["fixed_parameter_description"],
            data=fixed_param_data,
            value=settings.par1_name,
        )
    )
    technical.append(
        dmc.Box(create_par1_slider(param=par1, value=settings.par1_value, lang=lang), id="slider-par1-container")
    )
    technical.append(dbc.Row(style={"height": "30px"}))

    # Plot settings
    technical.append(sel.badge(dictionary["plot_settings"]))
    technical.append(
        sel.dropdown_with_title(
            dictionary["x_axis_parameter"],
            id="par2-dd",
            description=dictionary["x_axis_parameter_description"],
            data=SYSTEM_PARAMS.get_option_list_without_param(settings.par1_name, lang=lang),
            value=settings.par2_name,
        )
    )
    technical.append(
        dmc.MultiSelect(
            label=dictionary["y_axis_parameter"],
            description=dictionary["y_axis_parameter_description"],
            id="yaxis-multiselect",
            data=y_axis_params,
            value=settings.yaxis_names,
            maxValues=5,
            searchable=True,
            clearable=True,
            style={"width": "100%"},
        )
    )

    content.append(dmc.Box(technical, className="school-hidden" if school_mode else None))

    content.append(
        dmc.Switch(
            id="bjerrum-switch",
            label=dictionary["bjerrum_toggle"],
            checked=settings.show_bjerrum,
            size="sm",
            mt=8,
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
    compare_button = sel.button(
        "freeze-btn",
        dictionary["compare_stop"] if comparison_active else dictionary["compare_start"],
        "mdi:compare-horizontal",
        color=DMC_TEAL,
    )
    buttons = dmc.Stack(
        [
            dbc.Row(
                [
                    dbc.Col(reset_button, width=6),
                    dbc.Col(apply_button, width=6),
                ]
            ),
            dbc.Row(dbc.Col(compare_button, width=12), className="g-0 mt-1"),
        ]
    )
    content.append(buttons)

    # Share link and CSV download row
    content.append(
        dmc.Group(
            [
                dmc.Button(
                    dictionary["download_csv"],
                    id="csv-btn",
                    variant="subtle",
                    size="compact-sm",
                    color=DMC_GRAY,
                    leftSection=DashIconify(icon="mdi:file-delimited-outline", width=16),
                ),
                dmc.Group(
                    [
                        dmc.Text(dictionary["share_link"], size="sm", c="dimmed"),
                        dcc.Clipboard(
                            id="share-clipboard",
                            title=dictionary["share_link"],
                            style={"fontSize": "18px", "cursor": "pointer"},
                        ),
                    ],
                    gap="xs",
                ),
            ],
            justify="space-between",
            mt=8,
        )
    )

    # Mode switch: a plain link, so the target mode is reached with clean default settings.
    content.append(
        dmc.Anchor(
            dictionary["to_pro_mode"] if school_mode else dictionary["to_school_mode"],
            href=f"/?lang={lang}" if school_mode else f"/?mode=schule&lang={lang}",
            size="xs",
            c="dimmed",
            mt=4,
        )
    )

    # Final assembly the accordion
    accordion = sel.accordion_with_title(
        accordion_title, dmc.Stack(content, align="stretch", gap="xs"), icon="mdi:cog-outline", value=accordion_title
    )

    return accordion
