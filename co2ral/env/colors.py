# Mantine Colors
DMC_GRAY = "gray"
DMC_GREEN = "green"
DMC_RED = "red"
DMC_INDIGO = "indigo"
DMC_LIME = "lime"
DMC_TEAL = "teal"

# Hex Colors
GRAY = "#343A40"
GREEN = "#40C057"
RED = "#E03131"
INDIGO = "#3B5BDB"
LIME = "#66A80F"
TEAL = "#087F5B"

LIGHT_GREEN = "#00d26a"

# Change theme here
DMC_THEME = DMC_GREEN
THEME = GREEN

# Plot Colors -> same as defaults for apache e-charts
PLOT_COLORS = ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de"]


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Converts hex color to rgba color.

    :param hex_color: Hex color
    :param alpha: Alpha value, defaults to 1
    :return: RGBA color
    """
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"
