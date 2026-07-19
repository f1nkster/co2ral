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

# Fixed, deterministic positions (left %, top %) for the CO2 markers in the sky, so the
# picture does not jump around randomly whenever a value changes. They stay in the upper
# band, because the pCO2 label sits in the bottom left and the temperature badge top right.
_CO2_POSITIONS = [
    (6, 30),
    (16, 8),
    (25, 40),
    (34, 16),
    (44, 6),
    (52, 34),
    (61, 12),
    (70, 42),
    (78, 8),
    (86, 30),
    (4, 8),
    (12, 46),
    (21, 22),
    (30, 4),
    (40, 44),
    (49, 18),
    (58, 46),
    (66, 26),
    (75, 22),
    (83, 46),
    (90, 12),
    (36, 30),
    (55, 6),
    (72, 4),
]

# The picture keeps a light sky and a blue water body in both color schemes, so all text
# inside it needs explicit colors instead of the theme colors.
_TEXT_DARK = "#212529"
_TEXT_MUTED = "#5c636a"
_DELTA_COLORS = {"down": "#c92a2a", "up": "#0b7285", "none": "#868e96"}


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
        style={"backgroundColor": "#ffffff", "height": "100%"},
    )


def _coral_status(omega: float, lang: str) -> Component:
    """Builds the plain language verdict for the aragonite saturation.

    :param omega: Aragonite saturation state.
    :param lang: Selected language.
    :return: Alert-like band shown at the bottom of the water body.
    """
    dictionary = TRANSLATION_DICT[lang]
    if omega >= 3:
        text, background, border, icon = dictionary["ocean_coral_good"], "#e6fcf5", "#0ca678", "🪸"
    elif omega >= 1:
        text, background, border, icon = dictionary["ocean_coral_hard"], "#fff4e6", "#e8590c", "🪸"
    else:
        text, background, border, icon = dictionary["ocean_coral_bad"], "#fff5f5", "#c92a2a", "🐚"

    return dmc.Paper(
        dmc.Group(
            [dmc.Text(icon, style={"fontSize": "22px"}), dmc.Text(text, size="sm", fw=600, c=_TEXT_DARK)],
            gap="xs",
        ),
        p="xs",
        radius="md",
        mt="sm",
        style={"backgroundColor": background, "borderLeft": f"5px solid {border}"},
    )


def create_ocean_view(value_pco2: float, value_temperature: float, lang: str = "de") -> Component:
    """Builds the pictorial ocean view: sky with CO2, water body with the resulting values.

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

    # Sky: hazier the more CO2 is in the air. Water stays the same blue, so the numbers
    # and the coral verdict carry the message instead of a coloured-water suggestion.
    sky_fraction = (value_pco2 - PREINDUSTRIAL_PCO2) / (1200 - PREINDUSTRIAL_PCO2)
    sky_top = _interpolate_color((186, 226, 247), (214, 199, 170), sky_fraction)
    sky_bottom = _interpolate_color((222, 242, 252), (233, 223, 205), sky_fraction)
    temperature_color = _interpolate_color((77, 145, 214), (224, 90, 62), (value_temperature + 2) / 32)

    co2_count = min(max(round(value_pco2 / 50), 3), len(_CO2_POSITIONS))
    co2_markers = [
        html.Div(
            "CO₂",
            style={
                "position": "absolute",
                "left": f"{left}%",
                "top": f"{top}%",
                "fontSize": "11px",
                "fontWeight": 600,
                "color": "rgba(60, 60, 60, 0.75)",
                "backgroundColor": "rgba(255, 255, 255, 0.55)",
                "borderRadius": "8px",
                "padding": "1px 4px",
            },
        )
        for left, top in _CO2_POSITIONS[:co2_count]
    ]

    sky = html.Div(
        [
            *co2_markers,
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
                style={"position": "absolute", "left": "16px", "bottom": "12px"},
            ),
            dmc.Paper(
                dmc.Group(
                    [
                        html.Div(
                            style={
                                "width": "12px",
                                "height": "12px",
                                "borderRadius": "50%",
                                "backgroundColor": temperature_color,
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
                    "top": "12px",
                    "backgroundColor": "#ffffff",
                },
            ),
        ],
        style={
            "position": "relative",
            "height": "180px",
            "background": f"linear-gradient(to bottom, {sky_top}, {sky_bottom})",
            "borderTopLeftRadius": "12px",
            "borderTopRightRadius": "12px",
            "overflow": "hidden",
        },
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
            dmc.Text(dictionary["ocean_water"], size="xs", c="white", mb=6),
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
            _coral_status(current["saturation_aragonite"], lang),
        ],
        style={
            "background": "linear-gradient(to bottom, #1c7ed6, #0b4f8a)",
            "padding": "14px 16px 18px",
            "borderBottomLeftRadius": "12px",
            "borderBottomRightRadius": "12px",
        },
    )

    return html.Div([sky, water], style={"boxShadow": "0 2px 10px rgba(0, 0, 0, 0.15)", "borderRadius": "12px"})
