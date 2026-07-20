import dash_dynamic_grid_layout as dgl
from dash import html
from dash.development.base_component import Component


# Grid geometry. The 12-column grid matches bootstrap; the row height is small so resizing
# feels smooth, and the default tile height is chosen to fit a chart plus its title and
# subtitle without clipping.
GRID_COLUMNS = 12
ROW_HEIGHT = 20
GRID_MARGIN = 12
DEFAULT_TILE_HEIGHT = 22  # rows -> about 430 px with the margin above

# Wide panels span the full width by default, single-series line charts sit two per row.
_FULL_WIDTH_KEYS = ("speciation", "bjerrum")


def _tile_width(key: str) -> int:
    """Default width in grid columns for a plot, by its key.

    :param key: Stable plot key.
    :return: Width in columns.
    """
    return GRID_COLUMNS if key in _FULL_WIDTH_KEYS else GRID_COLUMNS // 2


def default_layout(keys: list[str]) -> list[dict]:
    """Builds the initial arrangement, flowing the tiles left to right and wrapping rows.

    :param keys: Stable plot keys in display order.
    :return: Layout list of {i, x, y, w, h} dicts.
    """
    layout = []
    x = 0
    y = 0
    for key in keys:
        width = _tile_width(key)
        if x + width > GRID_COLUMNS:
            x = 0
            y += DEFAULT_TILE_HEIGHT
        layout.append({"i": key, "x": x, "y": y, "w": width, "h": DEFAULT_TILE_HEIGHT})
        x += width
        if x >= GRID_COLUMNS:
            x = 0
            y += DEFAULT_TILE_HEIGHT
    return layout


def merge_layout(keys: list[str], stored: list[dict] | None) -> list[dict]:
    """Applies a remembered arrangement to the current set of plots.

    Plots the user has already positioned keep their place; plots that appear for the first
    time are given a default tile below the remembered ones, so a new y-axis selection never
    lands on top of an existing plot.

    :param keys: Stable plot keys currently shown, in display order.
    :param stored: Previously stored layout, or None.
    :return: Layout list covering exactly the current keys.
    """
    if not stored:
        return default_layout(keys)

    by_key = {entry["i"]: entry for entry in stored if entry.get("i") in keys}
    next_y = max((entry["y"] + entry["h"] for entry in by_key.values()), default=0)

    layout = []
    for key in keys:
        if key in by_key:
            entry = by_key[key]
            layout.append({"i": key, "x": entry["x"], "y": entry["y"], "w": entry["w"], "h": entry["h"]})
        else:
            layout.append({"i": key, "x": 0, "y": next_y, "w": _tile_width(key), "h": DEFAULT_TILE_HEIGHT})
            next_y += DEFAULT_TILE_HEIGHT
    return layout


def build_plot_grid(
    cells: list[tuple[str, Component]], stored_layout: list[dict] | None, handle_text: str, remount_token: str
) -> Component:
    """Wraps the plot cells in a draggable, resizable grid.

    react-grid-layout only reads itemLayout when the component mounts; on a plain prop update
    it keeps its own internal layout. That is what preserves a drag across a live value
    update. To apply a fresh layout — on reset or when the set of plots changes — the caller
    bumps the remount token, which changes the React key and forces a remount.

    :param cells: Pairs of (stable key, plot cell) in display order.
    :param stored_layout: Remembered arrangement to restore, or None for the default.
    :param handle_text: Localized label of the drag handle.
    :param remount_token: Value that stays constant across value-only updates and changes
        when the layout should be re-applied.
    :return: The grid component.
    """
    keys = [key for key, _ in cells]
    # Each itemLayout.i must match the id of its DraggableWrapper for the plot to keep its
    # position; the ids double as the stable keys used throughout.
    items = [
        dgl.DraggableWrapper(cell, id=key, handleText=handle_text, handleBackground="rgba(77,124,15,0.9)")
        for key, cell in cells
    ]

    grid = dgl.DashGridLayout(
        id="plot-grid",
        items=items,
        itemLayout=merge_layout(keys, stored_layout),
        rowHeight=ROW_HEIGHT,
        margin=[GRID_MARGIN, GRID_MARGIN],
        showRemoveButton=False,
        showResizeHandles=True,
        compactType="vertical",
        style={"width": "100%"},
    )
    # The grid component rejects a React key of its own, so the remount is forced one level
    # up: changing this wrapper's key remounts the subtree and applies itemLayout afresh.
    return html.Div(grid, key=remount_token)
