from core.utils.plot_grid import (
    DEFAULT_TILE_HEIGHT,
    GRID_COLUMNS,
    default_layout,
    merge_layout,
)


def test__default_layout__covers_all_keys_within_the_grid_width():
    """GIVEN a set of plot keys
    WHEN the default layout is built
    THEN every key gets a tile, and no tile exceeds the grid width
    """
    keys = ["speciation", "line-pH", "line-CO3", "line-HCO3"]

    layout = default_layout(keys)

    assert {entry["i"] for entry in layout} == set(keys)
    assert all(entry["x"] + entry["w"] <= GRID_COLUMNS for entry in layout)


def test__default_layout__wide_panels_span_the_full_width():
    """GIVEN the speciation and a line-chart key
    WHEN the default layout is built
    THEN the speciation panel spans the full width while a line chart takes half
    """
    layout = {entry["i"]: entry for entry in default_layout(["speciation", "line-pH"])}

    assert layout["speciation"]["w"] == GRID_COLUMNS
    assert layout["line-pH"]["w"] == GRID_COLUMNS // 2


def test__merge_layout__keeps_remembered_positions():
    """GIVEN a stored arrangement
    WHEN the layout is merged for the same keys
    THEN each plot keeps its stored position and size
    """
    stored = [
        {"i": "line-pH", "x": 6, "y": 0, "w": 6, "h": 10},
        {"i": "speciation", "x": 0, "y": 0, "w": 6, "h": 10},
    ]

    merged = {entry["i"]: entry for entry in merge_layout(["speciation", "line-pH"], stored)}

    assert merged["line-pH"] == {"i": "line-pH", "x": 6, "y": 0, "w": 6, "h": 10}
    assert merged["speciation"]["x"] == 0


def test__merge_layout__new_plot_is_placed_below_existing_ones():
    """GIVEN a stored arrangement and a newly added plot
    WHEN the layout is merged
    THEN the new plot is placed below the remembered tiles, never on top of them
    """
    stored = [{"i": "speciation", "x": 0, "y": 0, "w": 12, "h": 8}]

    merged = {entry["i"]: entry for entry in merge_layout(["speciation", "line-CO3"], stored)}

    assert merged["line-CO3"]["y"] >= stored[0]["y"] + stored[0]["h"]
    assert merged["line-CO3"]["h"] == DEFAULT_TILE_HEIGHT


def test__merge_layout__without_stored_falls_back_to_default():
    """GIVEN no stored arrangement
    WHEN the layout is merged
    THEN it equals the default layout
    """
    keys = ["speciation", "line-pH"]

    assert merge_layout(keys, None) == default_layout(keys)
    assert merge_layout(keys, []) == default_layout(keys)
