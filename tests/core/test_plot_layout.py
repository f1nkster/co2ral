from core.utils.plot_layout import (
    WIDTH_OPTIONS,
    build_plot_flow,
    default_width,
    order_keys,
    width_control,
)
from dash import html


def test__default_width__wide_panels_full_line_charts_half():
    """GIVEN wide-panel and line-chart keys
    WHEN their default width is derived
    THEN wide panels default to full width and line charts to a half
    """
    assert default_width("speciation") == "1"
    assert default_width("bjerrum") == "1"
    assert default_width("line-pH") == "2"


def test__order_keys__keeps_stored_order_and_appends_new():
    """GIVEN a stored order and a changed set of plots
    WHEN the keys are ordered
    THEN known keys keep the stored order and a new key is appended, not inserted
    """
    stored = ["line-pH", "speciation"]
    current = ["speciation", "line-pH", "line-CO3"]

    assert order_keys(current, stored) == ["line-pH", "speciation", "line-CO3"]


def test__order_keys__drops_stored_keys_that_disappeared():
    """GIVEN a stored order referencing a plot that is no longer shown
    WHEN the keys are ordered
    THEN the stale key is dropped and only current keys remain
    """
    stored = ["line-CO3", "speciation", "line-pH"]
    current = ["speciation", "line-pH"]

    assert order_keys(current, stored) == ["speciation", "line-pH"]


def test__order_keys__without_stored_keeps_input_order():
    """GIVEN no stored order
    WHEN the keys are ordered
    THEN the input order is returned unchanged
    """
    keys = ["speciation", "line-pH"]

    assert order_keys(keys, None) == keys
    assert order_keys(keys, []) == keys


def test__width_control__offers_all_options_and_reflects_the_value():
    """GIVEN a plot key and a current width value
    WHEN the width control is built
    THEN it offers every width option and starts on the given value
    """
    control = width_control("line-pH", "2")

    assert {option["value"] for option in control.data} == set(WIDTH_OPTIONS)
    assert control.value == "2"
    assert control.id == {"type": "tile-width", "key": "line-pH"}


def test__build_plot_flow__tags_each_tile_with_its_key_and_width():
    """GIVEN ordered cells and chosen widths
    WHEN the flow is built
    THEN each tile carries its data-key and the flex-basis of its chosen width
    """
    cells = [("speciation", html.Div("s")), ("line-pH", html.Div("p"))]
    widths = {"speciation": "1", "line-pH": "2"}

    flow = build_plot_flow(cells, widths)
    tiles = flow.children

    assert tiles[0].to_plotly_json()["props"]["data-key"] == "speciation"
    assert "100%" in tiles[0].style["flex"]
    assert "50%" in tiles[1].style["flex"]
