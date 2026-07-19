import pathlib
import re


ASSETS_DIR = pathlib.Path(__file__).resolve().parents[2] / "co2ral" / "assets"


def test__stylesheets__fetch_nothing_from_other_hosts():
    """GIVEN the stylesheets shipped in the assets folder
    WHEN they are scanned for references that trigger a request
    THEN none of them loads from another host, so the page stays free of external
         requests — the design was imported with its fonts self-hosted for this reason

    Only url() and @import count: links inside licence comments load nothing.
    """
    loading_reference = re.compile(r"""(?:url\(\s*['"]?|@import\s+(?:url\(\s*)?['"]?)(https?://[^\s"')]+)""")

    offenders = {}
    for stylesheet in sorted(ASSETS_DIR.glob("*.css")):
        external = loading_reference.findall(stylesheet.read_text(encoding="utf-8"))
        if external:
            offenders[stylesheet.name] = external[:3]

    assert not offenders, f"external references found: {offenders}"


def test__fonts__referenced_by_the_stylesheets_exist():
    """GIVEN the font faces declared in the stylesheets
    WHEN their file names are resolved in the assets folder
    THEN every referenced font file is actually present
    """
    missing = []
    for stylesheet in sorted(ASSETS_DIR.glob("*.css")):
        for reference in re.findall(r"url\((fonts/[^)]+)\)", stylesheet.read_text(encoding="utf-8")):
            if not (ASSETS_DIR / reference).is_file():
                missing.append(f"{stylesheet.name} -> {reference}")

    assert not missing, f"missing font files: {missing}"
