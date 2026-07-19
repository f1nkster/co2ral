import urllib.parse

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.utils.marine_model import run_single_state
from dash import html
from dash.development.base_component import Component
from locales.translation import TRANSLATION_DICT


# Pre-industrial CO2 level; every value is also shown as a difference to this reference
# state (at the same temperature), so students see what the CO2 rise alone has changed.
PREINDUSTRIAL_PCO2 = 280.0

# CO2 levels students can jump to directly.
PCO2_MILESTONES = {"ocean_1850": 280, "ocean_today": 420, "ocean_2100": 936}

# Fixed, deterministic positions (left %, top %, size px) of the CO2 markers, so the sky
# does not rearrange itself whenever a value changes. They stay in the upper band, because
# the pCO2 label sits bottom left and the temperature badge top right.
_CO2_POSITIONS = [
    (14, 30, 30),
    (26, 12, 26),
    (37, 34, 32),
    (48, 14, 27),
    (59, 32, 30),
    (69, 10, 25),
    (79, 30, 29),
    (88, 14, 26),
    (20, 48, 24),
    (33, 52, 27),
    (45, 46, 25),
    (57, 52, 28),
    (70, 46, 24),
    (82, 50, 27),
    (8, 12, 25),
    (17, 66, 22),
    (30, 70, 25),
    (43, 64, 23),
    (55, 70, 26),
    (66, 64, 22),
    (77, 68, 25),
    (90, 62, 23),
    (5, 44, 23),
    (95, 36, 22),
]

# Decorative clouds (left %, top %, width px, height px).
_CLOUDS = [(12, 16, 90, 26), (58, 8, 120, 30), (80, 34, 70, 20)]

# Decorative bubbles in the water (left %, bottom px, size px, delay s).
_BUBBLES = [(9, 20, 9, 0), (27, 0, 6, 2.5), (52, 30, 11, 5), (71, 10, 7, 1.5), (88, 25, 8, 3.8)]

# The picture keeps a light sky and a blue water body in both color schemes, so all text
# inside it needs explicit colors instead of the theme colors.
_TEXT_DARK = "#212529"
_TEXT_MUTED = "#5c636a"
_DELTA_COLORS = {"down": "#c92a2a", "up": "#0b7285", "none": "#868e96"}

_WATER_SURFACE = "#2f9bd6"
_WATER_GRADIENT = f"linear-gradient(180deg, {_WATER_SURFACE} 0%, #1a6fae 45%, #0b3f70 100%)"


def _svg_data_uri(svg: str) -> str:
    """Packs an inline svg into a css url() value, so no external file is requested.

    :param svg: The svg markup.
    :return: CSS url() value with the svg as data uri.
    """
    return f'url("data:image/svg+xml,{urllib.parse.quote(svg)}")'


def _wave_background(color: str) -> str:
    """Builds the repeating wave crest that forms the water surface.

    :param color: Fill color, matching the water surface.
    :return: CSS background-image value.
    """
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 22" preserveAspectRatio="none">'
        f'<path d="M0 11 Q 15 0 30 11 T 60 11 T 90 11 T 120 11 V22 H0 Z" fill="{color}"/>'
        f'<path d="M0 11 Q 15 0 30 11 T 60 11 T 90 11 T 120 11" fill="none" '
        'stroke="rgba(255,255,255,0.65)" stroke-width="1.5"/>'
        "</svg>"
    )
    return _svg_data_uri(svg)


def _coral_background(color: str) -> str:
    """Builds the stylized coral whose color reflects the aragonite saturation.

    :param color: Branch color of the coral.
    :return: CSS background-image value.
    """
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        f'<g stroke="{color}" stroke-width="6" stroke-linecap="round" fill="none">'
        '<path d="M32 62 V40"/><path d="M32 46 L21 33"/><path d="M32 46 L43 33"/>'
        '<path d="M21 33 L17 21"/><path d="M43 33 L47 21"/><path d="M32 40 L32 26"/>'
        '<path d="M32 30 L26 22"/><path d="M32 30 L38 22"/>'
        "</g></svg>"
    )
    return _svg_data_uri(svg)


def _format_number(value: float, decimals: int, lang: str) -> str:
    """Formats a number with the decimal separator of the given language.

    :param value: Value to format.
    :param decimals: Number of decimal places.
    :param lang: Language, "de" uses a decimal comma.
    :return: Formatted number.
    """
    text = f"{value:.{decimals}f}"
    return text.replace(".", ",") if lang == "de" else text


def _interpolate_color(start: tuple[int, int, int], end: tuple[int, int, int], fraction: float) -> str:
    """Interpolates linearly between two rgb colors.

    :param start: Color at fraction 0.
    :param end: Color at fraction 1.
    :param fraction: Position between both colors, clamped to [0, 1].
    :return: CSS rgb string.
    """
    fraction = min(max(fraction, 0.0), 1.0)
    channels = [round(s + (e - s) * fraction) for s, e in zip(start, end, strict=False)]
    return f"rgb({channels[0]}, {channels[1]}, {channels[2]})"


def _delta_text(current: float, reference: float, decimals: int, lang: str) -> tuple[str, str]:
    """Builds the change indicator of a value relative to the pre-industrial reference.

    :param current: Current value.
    :param reference: Reference value.
    :param decimals: Number of decimal places.
    :param lang: Selected language.
    :return: Tuple of label text and color.
    """
    difference = current - reference
    if abs(difference) < 0.5 * 10**-decimals:
        return ("±0", _DELTA_COLORS["none"])
    arrow = "▲" if difference > 0 else "▼"
    color = _DELTA_COLORS["down"] if difference < 0 else _DELTA_COLORS["up"]
    return (f"{arrow} {_format_number(abs(difference), decimals, lang)}", color)


def _value_card(label: str, value: str, unit: str, delta: tuple[str, str], lang: str, note: str = "") -> Component:
    """Builds a single value tile shown in the water body.

    :param label: Plain language name of the quantity.
    :param value: Formatted value.
    :param unit: Unit, may be empty.
    :param delta: Tuple of change text and color.
    :param lang: Selected language.
    :param note: Optional short explanation below the value.
    :return: Card component.
    """
    delta_text, delta_color = delta
    return dmc.Paper(
        [
            dmc.Text(label, size="xs", c=_TEXT_MUTED),
            dmc.Group(
                [
                    dmc.Text(value, fw=700, c=_TEXT_DARK, style={"fontSize": "26px", "lineHeight": "1.1"}),
                    dmc.Text(unit, size="xs", c=_TEXT_MUTED),
                ],
                gap=4,
                align="baseline",
            ),
            dmc.Group(
                [
                    dmc.Text(delta_text, size="xs", c=delta_color, fw=700),
                    dmc.Text(TRANSLATION_DICT[lang]["ocean_vs_1850"], size="xs", c=_TEXT_MUTED),
                ],
                gap=4,
            ),
            dmc.Text(note, size="xs", c=_TEXT_MUTED) if note else None,
        ],
        p="xs",
        radius="md",
        withBorder=True,
        className="ocean-card",
        style={"height": "100%"},
    )


def _coral_status(omega: float, lang: str) -> Component:
    """Builds the sea floor with a coral whose color reflects the aragonite saturation,
       together with the plain language verdict.

    :param omega: Aragonite saturation state.
    :param lang: Selected language.
    :return: Sea floor band closing the scene at the bottom.
    """
    dictionary = TRANSLATION_DICT[lang]
    # Vivid pink when calcification works, pale when it gets harder, gray skeleton when
    # calcium carbonate dissolves. Gray rather than white, so it stays visible on the sand.
    if omega >= 3:
        text, coral_color = dictionary["ocean_coral_good"], "#e64980"
    elif omega >= 1:
        text, coral_color = dictionary["ocean_coral_hard"], "#ffa8a8"
    else:
        text, coral_color = dictionary["ocean_coral_bad"], "#adb5bd"

    return html.Div(
        dmc.Group(
            [
                html.Div(
                    className="ocean-coral",
                    style={
                        "width": "74px",
                        "height": "74px",
                        "backgroundImage": _coral_background(coral_color),
                    },
                ),
                dmc.Text(text, size="sm", fw=600, c="#4a3f2a", style={"flex": "1"}),
            ],
            gap="sm",
            wrap="nowrap",
        ),
        className="ocean-floor ocean-content",
        style={"marginTop": "16px", "padding": "12px 18px 10px"},
    )


def create_ocean_view(value_pco2: float, value_temperature: float, lang: str = "de") -> Component:
    """Builds the pictorial ocean view: a sky whose haze and CO2 markers grow with the CO2
       level, above a water body showing the resulting values.

    Every value is shown together with its change relative to the pre-industrial reference
    at the same temperature, so the effect of moving one slider is directly readable.

    :param value_pco2: CO2 partial pressure in the air, in μatm.
    :param value_temperature: Water temperature in °C.
    :param lang: Selected language.
    :return: The complete picture as a component.
    """
    dictionary = TRANSLATION_DICT[lang]
    current = run_single_state(value_pco2=value_pco2, value_temperature=value_temperature)
    reference = run_single_state(value_pco2=PREINDUSTRIAL_PCO2, value_temperature=value_temperature)

    co2_fraction = min(max((value_pco2 - PREINDUSTRIAL_PCO2) / (1200 - PREINDUSTRIAL_PCO2), 0.0), 1.0)
    temperature_fraction = min(max((value_temperature + 2) / 34, 0.0), 1.0)

    # A warm sun for warm water, a pale one for cold water.
    sun_color = _interpolate_color((255, 249, 219), (255, 214, 153), temperature_fraction)
    sun_glow = _interpolate_color((255, 236, 179), (255, 167, 89), temperature_fraction)
    temperature_dot = _interpolate_color((77, 145, 214), (224, 90, 62), temperature_fraction)

    sky = html.Div(
        [
            html.Div(
                className="ocean-sun",
                style={
                    "left": "7%",
                    "top": "12%",
                    "width": "76px",
                    "height": "76px",
                    "background": f"radial-gradient(circle, #ffffff 8%, {sun_color} 45%, rgba(255,255,255,0) 72%)",
                    "boxShadow": f"0 0 46px 18px {sun_glow}",
                    "opacity": 0.95 - 0.25 * co2_fraction,
                },
            ),
            *[
                html.Div(
                    className="ocean-cloud",
                    style={"left": f"{left}%", "top": f"{top}%", "width": f"{width}px", "height": f"{height}px"},
                )
                for left, top, width, height in _CLOUDS
            ],
            # Smog wash: the more CO2, the hazier and warmer the sky gets.
            html.Div(
                className="ocean-haze",
                style={
                    "background": "linear-gradient(180deg, rgba(198,166,116,0) 0%, rgba(198,166,116,0.85) 100%)",
                    "opacity": co2_fraction,
                },
            ),
            *[
                html.Div(
                    "CO₂",
                    className="ocean-co2",
                    style={
                        "left": f"{left}%",
                        "top": f"{top}%",
                        "width": f"{size}px",
                        "height": f"{size}px",
                        "fontSize": f"{max(9, round(size * 0.34))}px",
                        "animationDelay": f"{(index % 5) * 0.7}s",
                    },
                )
                for index, (left, top, size) in enumerate(_CO2_POSITIONS[: _co2_marker_count(value_pco2)])
            ],
            html.Div(
                [
                    dmc.Text(dictionary["ocean_atmosphere"], size="xs", c=_TEXT_MUTED),
                    dmc.Group(
                        [
                            dmc.Text(
                                f"{round(value_pco2)}",
                                fw=700,
                                c=_TEXT_DARK,
                                style={"fontSize": "34px", "lineHeight": "1.1"},
                            ),
                            dmc.Text("μatm pCO₂", size="xs", c=_TEXT_MUTED),
                        ],
                        gap=6,
                        align="baseline",
                    ),
                ],
                style={"position": "absolute", "left": "18px", "bottom": "26px", "zIndex": 2},
            ),
            dmc.Paper(
                dmc.Group(
                    [
                        html.Div(
                            style={
                                "width": "12px",
                                "height": "12px",
                                "borderRadius": "50%",
                                "backgroundColor": temperature_dot,
                            }
                        ),
                        dmc.Text(f"{_format_number(value_temperature, 0, lang)} °C", size="sm", fw=700, c=_TEXT_DARK),
                    ],
                    gap=6,
                ),
                p="xs",
                radius="md",
                style={
                    "position": "absolute",
                    "right": "16px",
                    "top": "14px",
                    "backgroundColor": "rgba(255, 255, 255, 0.92)",
                    "zIndex": 2,
                },
            ),
            html.Div(className="ocean-waves", style={"backgroundImage": _wave_background(_WATER_SURFACE)}),
        ],
        className="ocean-sky",
        style={"background": "linear-gradient(180deg, #a5d6ef 0%, #cbe9f8 55%, #e4f3fb 100%)"},
    )

    cards = [
        (
            dictionary["ocean_ph"],
            _format_number(current["pH"], 2, lang),
            "",
            _delta_text(current["pH"], reference["pH"], 2, lang),
            dictionary["ocean_ph_note"],
        ),
        (
            dictionary["ocean_omega"],
            _format_number(current["saturation_aragonite"], 2, lang),
            "",
            _delta_text(current["saturation_aragonite"], reference["saturation_aragonite"], 2, lang),
            "",
        ),
        (
            dictionary["ocean_co2_aq"],
            _format_number(current["CO2"], 1, lang),
            "μmol/kg",
            _delta_text(current["CO2"], reference["CO2"], 1, lang),
            "",
        ),
        (
            dictionary["ocean_co3"],
            _format_number(current["CO3"], 0, lang),
            "μmol/kg",
            _delta_text(current["CO3"], reference["CO3"], 0, lang),
            "",
        ),
        (
            dictionary["ocean_hco3"],
            _format_number(current["HCO3"], 0, lang),
            "μmol/kg",
            _delta_text(current["HCO3"], reference["HCO3"], 0, lang),
            "",
        ),
        (
            dictionary["ocean_dic"],
            _format_number(current["dic"], 0, lang),
            "μmol/kg",
            _delta_text(current["dic"], reference["dic"], 0, lang),
            "",
        ),
    ]

    water = html.Div(
        [
            html.Div(className="ocean-rays"),
            *[
                html.Div(
                    className="ocean-bubble",
                    style={
                        "left": f"{left}%",
                        "bottom": f"{bottom}px",
                        "width": f"{size}px",
                        "height": f"{size}px",
                        "animationDelay": f"{delay}s",
                    },
                )
                for left, bottom, size, delay in _BUBBLES
            ],
            html.Div(
                [
                    dmc.Text(dictionary["ocean_water"], size="xs", c="rgba(255,255,255,0.85)", mb=8),
                    dbc.Row(
                        [
                            dbc.Col(
                                _value_card(label, value, unit, delta, lang, note),
                                xs=6,
                                md=4,
                                className="mb-2",
                            )
                            for label, value, unit, delta, note in cards
                        ],
                        className="g-2",
                    ),
                ],
                className="ocean-content",
                style={"padding": "16px 16px 0"},
            ),
            _coral_status(current["saturation_aragonite"], lang),
        ],
        className="ocean-water",
        style={"background": _WATER_GRADIENT},
    )

    return html.Div([sky, water], className="ocean-scene")


def _co2_marker_count(value_pco2: float) -> int:
    """Number of CO2 markers drawn in the sky for a given CO2 level.

    :param value_pco2: CO2 partial pressure in μatm.
    :return: Marker count within the available positions.
    """
    return min(max(round(value_pco2 / 50), 3), len(_CO2_POSITIONS))
