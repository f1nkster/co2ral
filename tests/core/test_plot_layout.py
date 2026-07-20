from core.utils.plot_layout import build_plot_flow, default_rows, layout_rows
from dash import html


def test__default_rows__wide_panels_alone_line_charts_paired():
    """GIVEN wide-panel and line-chart keys
    WHEN the default arrangement is built
    THEN wide panels get a row of their own and line charts pair up two to a row
    """
    keys = ["speciation", "bjerrum", "line-pH", "line-CO3", "line-fCO2"]

    assert default_rows(keys) == [["speciation"], ["bjerrum"], ["line-pH", "line-CO3"], ["line-fCO2"]]


def test__layout_rows__without_stored_builds_the_default():
    """GIVEN no stored arrangement
    WHEN the rows are laid out
    THEN the default arrangement is returned
    """
    keys = ["speciation", "line-pH"]

    assert layout_rows(keys, None) == default_rows(keys)
    assert layout_rows(keys, []) == default_rows(keys)


def test__layout_rows__keeps_stored_rows_and_appends_new_keys():
    """GIVEN a stored arrangement and a plot that appears for the first time
    WHEN the rows are laid out
    THEN known keys keep their rows and the new key gets a row of its own at the end
    """
    stored = [["line-pH", "speciation"], ["line-CO3"]]
    current = ["speciation", "line-pH", "line-CO3", "line-fCO2"]

    assert layout_rows(current, stored) == [["line-pH", "speciation"], ["line-CO3"], ["line-fCO2"]]


def test__layout_rows__drops_stored_keys_that_disappeared():
    """GIVEN a stored arrangement referencing a plot that is no longer shown
    WHEN the rows are laid out
    THEN the stale key is dropped and its emptied row disappears
    """
    stored = [["line-CO3"], ["speciation", "line-pH"]]
    current = ["speciation", "line-pH"]

    assert layout_rows(current, stored) == [["speciation", "line-pH"]]


def test__layout_rows__splits_over_full_rows():
    """GIVEN a stale stored arrangement with three plots in one row
    WHEN the rows are laid out
    THEN the row is split so no row holds more than two plots
    """
    stored = [["speciation", "line-pH", "line-CO3"]]
    current = ["speciation", "line-pH", "line-CO3"]

    assert layout_rows(current, stored) == [["speciation", "line-pH"], ["line-CO3"]]


def test__build_plot_flow__tags_each_tile_with_its_key_and_groups_rows():
    """GIVEN rows of cells
    WHEN the flow is built
    THEN each row becomes a container whose tiles carry their data-key
    """
    rows = [
        [("speciation", html.Div("s"))],
        [("line-pH", html.Div("p")), ("line-CO3", html.Div("c"))],
    ]

    flow = build_plot_flow(rows)

    assert [len(row.children) for row in flow.children] == [1, 2]
    first_tile = flow.children[0].children[0]
    assert first_tile.to_plotly_json()["props"]["data-key"] == "speciation"
    assert first_tile.className == "plot-tile"
    assert flow.children[1].className == "plot-row"
