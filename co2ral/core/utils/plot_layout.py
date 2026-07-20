import dash_mantine_components as dmc
from dash import html
from dash.development.base_component import Component


# Selectable tile widths as a fraction of a row: half, third, full.
WIDTH_OPTIONS = ("2", "3", "1")  # value = denominator; "1" means full width
DEFAULT_WIDTH = "1"

# Flex row gap in px; the tile widths subtract their share of it so the columns fit exactly.
GRID_GAP = 16

# Width as a calc that accounts for the gap: n tiles of `100/n % - (n-1)/n * gap` plus the
# gaps between them fill the row precisely.
WIDTH_BASIS = {
    "1": "100%",
    "2": f"calc(50% - {GRID_GAP / 2:g}px)",
    "3": f"calc(33.333% - {GRID_GAP * 2 / 3:g}px)",
}

# Wide panels default to the full width, single-series line charts to a half.
_DEFAULT_HALF_KEYS_PREFIX = "line-"


def default_width(key: str) -> str:
    """Default width value for a plot, by its key.

    :param key: Stable plot key.
    :return: A value from WIDTH_OPTIONS.
    """
    return "2" if key.startswith(_DEFAULT_HALF_KEYS_PREFIX) else "1"


def order_keys(keys: list[str], stored_order: list[str] | None) -> list[str]:
    """Applies a remembered order to the current set of plots.

    Plots the user has already arranged keep their order; plots that appear for the first
    time are appended, so a new y-axis selection never reshuffles the existing tiles.

    :param keys: Stable plot keys currently shown.
    :param stored_order: Previously stored order, or None.
    :return: The keys in display order.
    """
    if not stored_order:
        return keys
    known = [key for key in stored_order if key in keys]
    new = [key for key in keys if key not in known]
    return known + new


def width_control(key: str, value: str) -> Component:
    """Builds the per-tile width selector shown in the plot header.

    :param key: Stable plot key, used in the control id.
    :param value: Currently selected width value.
    :return: A segmented control switching the tile between half, third and full width.
    """
    labels = {"1": "1", "2": "½", "3": "⅓"}
    return dmc.SegmentedControl(
        id={"type": "tile-width", "key": key},
        data=[{"value": option, "label": labels[option]} for option in WIDTH_OPTIONS],
        value=value if value in WIDTH_OPTIONS else DEFAULT_WIDTH,
        size="xs",
        className="tile-width-control",
    )


def build_plot_flow(cells: list[tuple[str, Component]], widths: dict[str, str]) -> Component:
    """Arranges the plot cells in a flowing, reorderable row layout.

    Each tile takes its chosen fraction of the row width and the tiles wrap into rows, so
    two half-width plots share a row and a full-width plot takes the next — the arrangement
    the user composes by setting widths and dragging tiles by their header.

    :param cells: Pairs of (stable key, plot cell) already in display order.
    :param widths: Chosen width value per key.
    :return: The flow container.
    """
    tiles = []
    for key, cell in cells:
        width_value = widths.get(key, default_width(key))
        basis = WIDTH_BASIS.get(width_value, "100%")
        tiles.append(
            html.Div(
                cell,
                className="plot-tile",
                # No grow, so a lone half-width tile stays half wide instead of stretching.
                style={"flex": f"0 1 {basis}", "width": basis},
                **{"data-key": key},
            )
        )

    return html.Div(tiles, id="plot-flow", className="plot-flow")
