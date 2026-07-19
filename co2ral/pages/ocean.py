import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components import selection as sel
from core.utils.ocean_view import PCO2_MILESTONES, create_ocean_view
from dash import ALL, Input, Output, State, callback, ctx, dcc, html
from dash.development.base_component import Component
from env.colors import DMC_TEAL
from locales.translation import TRANSLATION_DICT


dash.register_page(__name__, path="/ozean", name="Ocean")

PCO2_MIN = 280
PCO2_MAX = 1200
TEMPERATURE_MIN = 0
TEMPERATURE_MAX = 32


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


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the pictorial ocean view.

    :param url_queries: The url arguments: lang, co2 and temp.
    :return: Layout with the two sliders and the picture.
    """
    lang = url_queries.get("lang", "de")
    if lang not in TRANSLATION_DICT:
        lang = "de"
    dictionary = TRANSLATION_DICT[lang]

    value_pco2 = min(max(_to_number(url_queries.get("co2"), 420), PCO2_MIN), PCO2_MAX)
    value_temperature = min(max(_to_number(url_queries.get("temp"), 18), TEMPERATURE_MIN), TEMPERATURE_MAX)

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
        # Clear the slider's mark labels, which extend below the track.
        mt=30,
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
            ),
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
            html.Div(id="ocean-view", children=create_ocean_view(value_pco2, value_temperature, lang)),
            dmc.Text(dictionary["ocean_hint_ph"], size="xs", c="dimmed", mt="xs"),
            dmc.Anchor(dictionary["ocean_back"], href=f"/?mode=schule&lang={lang}", size="sm"),
            dcc.Store(id="ocean-lang-store", data=lang),
        ],
        gap="sm",
    )

    return dbc.Container(
        dbc.Row(dbc.Col(content, xs=12, lg=10, xl=8)),
        fluid=True,
        style={"paddingTop": "20px", "paddingBottom": "40px"},
    )


@callback(
    Output("ocean-view", "children"),
    [
        Input("ocean-pco2", "value"),
        Input("ocean-temp", "value"),
    ],
    State("ocean-lang-store", "data"),
)
def update_ocean_view(value_pco2: float, value_temperature: float, lang: str) -> Component:
    """Recalculates and redraws the picture whenever a slider changes.

    :param value_pco2: CO2 partial pressure in the air, in μatm.
    :param value_temperature: Water temperature in °C.
    :param lang: Selected language.
    :return: The updated picture.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    if value_pco2 is None or value_temperature is None:
        return dash.no_update
    return create_ocean_view(value_pco2=value_pco2, value_temperature=value_temperature, lang=lang)


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
