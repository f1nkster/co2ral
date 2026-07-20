from dash import html
from dash.development.base_component import Component


# A row holds one tile (full width) or two (half width each); where a tile is dropped
# decides which — there is no explicit width control.
MAX_TILES_PER_ROW = 2

# Single-series line charts pair up two to a row by default; the wide panels
# (speciation, Bjerrum) get a row — and so the full width — of their own.
_PAIRED_KEYS_PREFIX = "line-"


def default_rows(keys: list[str]) -> list[list[str]]:
    """Builds the default arrangement for the given plots.

    :param keys: Stable plot keys in display order.
    :return: Rows of keys — wide panels alone, line charts paired in order.
    """
    rows: list[list[str]] = []
    pending: list[str] = []
    for key in keys:
        if key.startswith(_PAIRED_KEYS_PREFIX):
            pending.append(key)
            if len(pending) == MAX_TILES_PER_ROW:
                rows.append(pending)
                pending = []
        else:
            if pending:
                rows.append(pending)
                pending = []
            rows.append([key])
    if pending:
        rows.append(pending)
    return rows


def layout_rows(keys: list[str], stored_rows: list[list[str]] | None) -> list[list[str]]:
    """Applies the remembered arrangement to the current set of plots.

    Plots the user has already arranged keep their row; plots that appear for the first
    time are appended in rows of their own, so a new y-axis selection never reshuffles
    the existing tiles.

    :param keys: Stable plot keys currently shown.
    :param stored_rows: Previously stored rows of keys, or None for the default.
    :return: Rows of keys, each holding at most MAX_TILES_PER_ROW.
    """
    if not stored_rows:
        return default_rows(keys)

    current = set(keys)
    rows: list[list[str]] = []
    known: set[str] = set()
    for stored_row in stored_rows:
        row = [key for key in stored_row if key in current and key not in known]
        known.update(row)
        # A stale store may hold over-full rows; split them instead of failing.
        for start in range(0, len(row), MAX_TILES_PER_ROW):
            rows.append(row[start : start + MAX_TILES_PER_ROW])
    rows = [row for row in rows if row]
    rows.extend([key] for key in keys if key not in known)
    return rows


def build_plot_flow(rows: list[list[tuple[str, Component]]]) -> Component:
    """Arranges the plot cells in stacked, reorderable rows.

    The tiles in a row share its width equally, so a lone tile spans the full width and
    two tiles snap to half each — the arrangement the user composes by dragging tiles
    next to each other or into the drop zone between two rows. The drop zones themselves
    are inserted client-side (assets/11-plot-rows.js), which also attaches the dragging.

    :param rows: Rows of (stable key, plot cell) pairs, already in display order.
    :return: The flow container.
    """
    row_divs = []
    for row in rows:
        tiles = [html.Div(cell, className="plot-tile", **{"data-key": key}) for key, cell in row]
        row_divs.append(html.Div(tiles, className="plot-row"))
    return html.Div(row_divs, id="plot-flow", className="plot-flow")
