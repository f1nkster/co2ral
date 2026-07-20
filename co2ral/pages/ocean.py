import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components import selection as sel
from core.utils.climate import (
    PREINDUSTRIAL_SEA_SURFACE_TEMPERATURE,
    SEA_SURFACE_WARMING_PER_DOUBLING,
    coupled_temperature,
)
from core.utils.ocean_view import PCO2_MILESTONES, create_ocean_view
from core.utils.particles import create_particle_view
from dash import ALL, Input, Output, State, callback, ctx, dcc, html
from dash.development.base_component import Component
from env.colors import DMC_TEAL
from locales.translation import TRANSLATION_DICT


dash.register_page(__name__, path="/ozean", name="Ocean")

PCO2_MIN = 280
PCO2_MAX = 1200
TEMPERATURE_MIN = 0
TEMPERATURE_MAX = 32

# Distance that clears the mark labels below a slider track.
_BELOW_SLIDER = 30


def _to_number(value: object, fallback: float) -> float:
    """Parses a url value to a number, falling back on invalid input.

    :param value: Raw query value.
    :param fallback: Value to use if parsing fails.
    :return: Parsed number or fallback.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _climate_note(climate_active: bool, lang: str) -> Component | None:
    """Names the coupling assumption whenever the coupling is switched on.

    :param climate_active: Whether the climate coupling is active.
    :param lang: Selected language.
    :return: Note component, or None while the coupling is off.
    """
    if not climate_active:
        return None

    numbers = {
        "warming": f"{SEA_SURFACE_WARMING_PER_DOUBLING:g}",
        "baseline": f"{PREINDUSTRIAL_SEA_SURFACE_TEMPERATURE:g}",
    }
    if lang == "de":
        numbers = {key: value.replace(".", ",") for key, value in numbers.items()}

    return dmc.Text(TRANSLATION_DICT[lang]["climate_note_template"].format(**numbers), size="xs", c="dimmed", mt=4)


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the pictorial ocean view.

    :param url_queries: The url arguments: lang, co2, temp and climate.
    :return: Layout with the sliders, the picture and the particle model.
    """
    lang = url_queries.get("lang", "de")
    if lang not in TRANSLATION_DICT:
        lang = "de"
    dictionary = TRANSLATION_DICT[lang]

    value_pco2 = min(max(_to_number(url_queries.get("co2"), 420), PCO2_MIN), PCO2_MAX)
    value_temperature = min(max(_to_number(url_queries.get("temp"), 18), TEMPERATURE_MIN), TEMPERATURE_MAX)
    climate_active = str(url_queries.get("climate", "")).lower() in ("1", "true")
    if climate_active:
        value_temperature = coupled_temperature(value_pco2, TEMPERATURE_MIN, TEMPERATURE_MAX)

    milestones = dmc.Group(
        [dmc.Text(dictionary["ocean_jump"], size="xs", c="dimmed")]
        + [
            dmc.Button(
                f"{dictionary[key]} ({value} μatm)",
                id={"type": "pco2-jump", "value": value},
                variant="light",
                size="compact-xs",
                color=DMC_TEAL,
                n_clicks=0,
            )
            for key, value in PCO2_MILESTONES.items()
        ],
        gap="xs",
        mt=_BELOW_SLIDER,
    )

    controls = dmc.Paper(
        [
            sel.range_slider(
                id="ocean-pco2",
                name=dictionary["ocean_co2_slider"],
                sub_text="μatm",
                value=value_pco2,
                min_val=PCO2_MIN,
                max_val=PCO2_MAX,
                step=20,
            ),
            milestones,
            dbc.Row(style={"height": "26px"}),
            sel.range_slider(
                id="ocean-temp",
                name=dictionary["ocean_temp_slider"],
                sub_text="°C",
                value=value_temperature,
                min_val=TEMPERATURE_MIN,
                max_val=TEMPERATURE_MAX,
                step=1,
                disabled=climate_active,
            ),
            dmc.Switch(
                id="climate-switch",
                label=dictionary["climate_toggle"],
                description=dictionary["climate_toggle_hint"],
                checked=climate_active,
                size="sm",
                mt=_BELOW_SLIDER,
            ),
            html.Div(id="climate-note", children=_climate_note(climate_active, lang)),
        ],
        p="md",
        radius="md",
        withBorder=True,
        mb="md",
    )

    content = dmc.Stack(
        [
            dmc.Title(dictionary["ocean_title"], order=2),
            dmc.Text(dictionary["ocean_intro"], size="sm"),
            controls,
            html.Div(
                id="ocean-view",
                children=[
                    create_ocean_view(value_pco2, value_temperature, lang),
                    create_particle_view(value_pco2, value_temperature, lang),
                ],
            ),
            dmc.Text(dictionary["ocean_hint_ph"], size="xs", c="dimmed", mt="xs"),
            dmc.Text(dictionary["ocean_warming_hint"], size="xs", c="dimmed"),
            dmc.Anchor(dictionary["ocean_back"], href=f"/?mode=schule&lang={lang}", size="sm"),
            dcc.Store(id="ocean-lang-store", data=lang),
        ],
        gap="sm",
    )

    return dbc.Container(
        dbc.Row(dbc.Col(content, xs=12, lg=10, xl=8), justify="center"),
        fluid=True,
        style={"paddingTop": "20px", "paddingBottom": "40px"},
    )


@callback(
    [
        Output("ocean-temp", "value"),
        Output("ocean-temp", "disabled"),
        Output("climate-note", "children"),
    ],
    [
        Input("ocean-pco2", "value"),
        Input("climate-switch", "checked"),
    ],
    State("ocean-lang-store", "data"),
)
def apply_climate_coupling(value_pco2: float, climate_active: bool, lang: str) -> tuple:
    """Lets the temperature follow the CO2 level while the coupling is switched on.

    The slider is disabled in that case, because its value is then derived rather than
    chosen — otherwise students could set a combination the coupling contradicts.

    :param value_pco2: Current CO2 value.
    :param climate_active: Whether the climate coupling is active.
    :param lang: Selected language.
    :return: Temperature, disabled flag and the note naming the assumption.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    if value_pco2 is None:
        return (dash.no_update, dash.no_update, dash.no_update)

    if not climate_active:
        return (dash.no_update, False, None)

    return (
        coupled_temperature(value_pco2, TEMPERATURE_MIN, TEMPERATURE_MAX),
        True,
        _climate_note(True, lang),
    )


@callback(
    Output("ocean-view", "children"),
    [
        Input("ocean-pco2", "value"),
        Input("ocean-temp", "value"),
    ],
    State("ocean-lang-store", "data"),
)
def update_ocean_view(value_pco2: float, value_temperature: float, lang: str) -> list:
    """Redraws the picture and the particle model whenever a slider changes.

    :param value_pco2: CO2 partial pressure in the air, in μatm.
    :param value_temperature: Water temperature in °C.
    :param lang: Selected language.
    :return: Children of the view container.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    if value_pco2 is None or value_temperature is None:
        return dash.no_update

    return [
        create_ocean_view(value_pco2, value_temperature, lang),
        create_particle_view(value_pco2, value_temperature, lang),
    ]


@callback(
    Output("ocean-pco2", "value"),
    Input({"type": "pco2-jump", "value": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def jump_to_milestone(n_clicks_list: list[int]) -> float:
    """Sets the CO2 slider to a milestone value (pre-industrial, today, possible future).

    :param n_clicks_list: Click counts of all milestone buttons.
    :return: The chosen CO2 value.
    """
    if not ctx.triggered_id or not any(n_clicks_list or []):
        return dash.no_update
    return ctx.triggered_id["value"]
