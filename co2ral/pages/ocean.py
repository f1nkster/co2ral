import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.components import selection as sel
from core.utils.marine_model import run_single_state
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

# The quantity a student predicts depends on the slider they moved, together with the
# number of decimals shown for it: the prediction is checked against the displayed value.
_SLIDER_QUANTITY = {"ocean-pco2": "pH", "ocean-temp": "CO2"}
_QUANTITY_DECIMALS = {"pH": 2, "CO2": 1}
_QUANTITY_QUESTION = {"pH": "predict_q_ph", "CO2": "predict_q_co2"}
_EXPLANATIONS = {
    ("pH", "down"): "predict_expl_ph_down",
    ("pH", "up"): "predict_expl_ph_up",
    ("CO2", "down"): "predict_expl_co2_down",
    ("CO2", "up"): "predict_expl_co2_up",
}
_ANSWER_OPTIONS = [("up", "predict_up"), ("same", "predict_same"), ("down", "predict_down")]


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


def _default_store(active: bool, value_pco2: float, value_temperature: float) -> dict:
    """Builds the initial prediction state.

    :param active: Whether prediction mode is switched on.
    :param value_pco2: Current CO2 value.
    :param value_temperature: Current temperature value.
    :return: Prediction store content.
    """
    return {
        "active": bool(active),
        "phase": "idle",
        "quantity": "pH",
        "correct": "same",
        "chosen": None,
        "pco2": value_pco2,
        "temp": value_temperature,
    }


def _direction(previous: float, current: float, decimals: int) -> str:
    """Compares two values as they are displayed, so a prediction is judged against
       what the student can actually read off.

    :param previous: Value before the change.
    :param current: Value after the change.
    :param decimals: Decimals the value is displayed with.
    :return: "up", "down" or "same".
    """
    before, after = round(previous, decimals), round(current, decimals)
    if after > before:
        return "up"
    if after < before:
        return "down"
    return "same"


def _prediction_card(store: dict, lang: str) -> Component:
    """Builds the question or the feedback of the prediction mode.

    :param store: Current prediction state.
    :param lang: Selected language.
    :return: Card component, or an idle hint when nothing is pending.
    """
    dictionary = TRANSLATION_DICT[lang]

    if store["phase"] == "asking":
        return dmc.Paper(
            [
                dmc.Text(dictionary[_QUANTITY_QUESTION[store["quantity"]]], fw=700, size="md"),
                dmc.Group(
                    [
                        dmc.Button(
                            dictionary[label_key],
                            id={"type": "predict-answer", "value": value},
                            n_clicks=0,
                            variant="light",
                            color=DMC_TEAL,
                            size="md",
                        )
                        for value, label_key in _ANSWER_OPTIONS
                    ],
                    gap="xs",
                    mt="xs",
                ),
            ],
            p="md",
            radius="md",
            withBorder=True,
            mb="md",
        )

    if store["phase"] == "answered":
        is_correct = store["chosen"] == store["correct"]
        explanation_key = _EXPLANATIONS.get((store["quantity"], store["correct"]), "predict_expl_same")
        return dmc.Alert(
            dmc.Text(dictionary[explanation_key], size="sm"),
            title=dictionary["predict_correct"] if is_correct else dictionary["predict_wrong"],
            color="teal" if is_correct else "orange",
            radius="md",
            mb="md",
        )

    return dmc.Text(dictionary["predict_toggle_hint"], size="xs", c="dimmed", mb="xs")


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the pictorial ocean view.

    :param url_queries: The url arguments: lang, co2, temp and predict.
    :return: Layout with the sliders, the picture and the particle model.
    """
    lang = url_queries.get("lang", "de")
    if lang not in TRANSLATION_DICT:
        lang = "de"
    dictionary = TRANSLATION_DICT[lang]

    value_pco2 = min(max(_to_number(url_queries.get("co2"), 420), PCO2_MIN), PCO2_MAX)
    value_temperature = min(max(_to_number(url_queries.get("temp"), 18), TEMPERATURE_MIN), TEMPERATURE_MAX)
    predict_active = str(url_queries.get("predict", "")).lower() in ("1", "true")

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
            dmc.Switch(
                id="predict-switch",
                label=dictionary["predict_toggle"],
                description=dictionary["predict_toggle_hint"],
                checked=predict_active,
                size="sm",
                mt="md",
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
            html.Div(
                id="ocean-view",
                children=[
                    create_ocean_view(value_pco2, value_temperature, lang),
                    create_particle_view(value_pco2, value_temperature, lang),
                ],
            ),
            dmc.Text(dictionary["ocean_hint_ph"], size="xs", c="dimmed", mt="xs"),
            dmc.Anchor(dictionary["ocean_back"], href=f"/?mode=schule&lang={lang}", size="sm"),
            dcc.Store(id="ocean-lang-store", data=lang),
            dcc.Store(id="predict-store", data=_default_store(predict_active, value_pco2, value_temperature)),
        ],
        gap="sm",
    )

    return dbc.Container(
        dbc.Row(dbc.Col(content, xs=12, lg=10, xl=8)),
        fluid=True,
        style={"paddingTop": "20px", "paddingBottom": "40px"},
    )


@callback(
    Output("predict-store", "data"),
    [
        Input("ocean-pco2", "value"),
        Input("ocean-temp", "value"),
        Input("predict-switch", "checked"),
        Input({"type": "predict-answer", "value": ALL}, "n_clicks"),
    ],
    State("predict-store", "data"),
)
def update_prediction(
    value_pco2: float,
    value_temperature: float,
    predict_active: bool,
    answer_clicks: list[int],
    store: dict,
) -> dict:
    """Drives the prediction cycle: moving a slider poses a question, answering reveals
       the values again. Without prediction mode the state simply follows the sliders.

    :param value_pco2: Current CO2 value.
    :param value_temperature: Current temperature value.
    :param predict_active: Whether prediction mode is switched on.
    :param answer_clicks: Click counts of the answer buttons.
    :param store: Previous prediction state.
    :return: Updated prediction state.
    """
    if value_pco2 is None or value_temperature is None:
        return dash.no_update

    store = dict(store or _default_store(predict_active, value_pco2, value_temperature))
    triggered = ctx.triggered_id
    triggered_value = ctx.triggered[0]["value"] if ctx.triggered else None

    # An answer was given: reveal the values together with the explanation.
    if isinstance(triggered, dict) and triggered.get("type") == "predict-answer" and triggered_value:
        store["phase"] = "answered"
        store["chosen"] = triggered["value"]
        return store

    # A slider moved while prediction mode is on: ask before showing the new values.
    if triggered in _SLIDER_QUANTITY and predict_active:
        quantity = _SLIDER_QUANTITY[triggered]
        previous = run_single_state(value_pco2=store["pco2"], value_temperature=store["temp"])
        current = run_single_state(value_pco2=value_pco2, value_temperature=value_temperature)
        store.update(
            phase="asking",
            quantity=quantity,
            correct=_direction(previous[quantity], current[quantity], _QUANTITY_DECIMALS[quantity]),
            chosen=None,
        )
    else:
        store["phase"] = "idle"

    store.update(active=bool(predict_active), pco2=value_pco2, temp=value_temperature)
    return store


@callback(
    Output("ocean-view", "children"),
    Input("predict-store", "data"),
    [
        State("ocean-pco2", "value"),
        State("ocean-temp", "value"),
        State("ocean-lang-store", "data"),
    ],
)
def update_ocean_view(store: dict, value_pco2: float, value_temperature: float, lang: str) -> list:
    """Redraws picture and particle model, masking the values while a prediction is pending.

    :param store: Current prediction state.
    :param value_pco2: CO2 partial pressure in the air, in μatm.
    :param value_temperature: Water temperature in °C.
    :param lang: Selected language.
    :return: Children of the view container.
    """
    lang = lang if lang in TRANSLATION_DICT else "de"
    if value_pco2 is None or value_temperature is None:
        return dash.no_update

    store = store or _default_store(False, value_pco2, value_temperature)
    is_asking = bool(store.get("active")) and store.get("phase") == "asking"

    children = []
    if store.get("active"):
        children.append(_prediction_card(store, lang))
    children.append(create_ocean_view(value_pco2, value_temperature, lang, hidden=is_asking))
    if not is_asking:
        children.append(create_particle_view(value_pco2, value_temperature, lang))
    return children


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
