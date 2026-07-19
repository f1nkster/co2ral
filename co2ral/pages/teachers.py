import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from core.utils.experiments import EXPERIMENTS
from core.utils.presets import SCHOOL_PRESETS
from dash import html
from dash.development.base_component import Component
from dash_iconify import DashIconify
from locales.translation import TRANSLATION_DICT


dash.register_page(__name__, path="/lehrkraefte", name="Teachers")

# Curriculum concept -> where it can be experienced in the app. The values are translation keys.
CURRICULUM_ROWS = [
    ("curr_dynamic", "curr_dynamic_where"),
    ("curr_lechatelier", "curr_lechatelier_where"),
    ("curr_acidbase", "curr_acidbase_where"),
    ("curr_solubility", "curr_solubility_where"),
    ("curr_buffer", "curr_buffer_where"),
]

TASK_KEYS = ["task_1", "task_2", "task_3", "task_4", "task_5"]


def _link_card(label: str, href: str, icon: str) -> Component:
    """Creates a full-width link button for a ready-made lesson state.

    :param label: Visible label of the link.
    :param href: Target url including all settings.
    :param icon: Iconify icon name.
    :return: Anchor wrapping a button.
    """
    return html.A(
        dmc.Button(
            label,
            variant="light",
            color="teal",
            fullWidth=True,
            styles={"label": {"whiteSpace": "normal", "textAlign": "left"}},
            leftSection=DashIconify(icon=icon, width=18),
            mb=6,
        ),
        href=href,
        style={"textDecoration": "none"},
    )


def layout(**url_queries: dict) -> Component:
    """Returns the layout for the teacher material page.

    :param url_queries: The url arguments, only lang is used.
    :return: Layout with curriculum table, ready-made lesson links and task suggestions.
    """
    lang = url_queries.get("lang", "de")
    if lang not in TRANSLATION_DICT:
        lang = "de"
    dictionary = TRANSLATION_DICT[lang]

    curriculum_table = dmc.Table(
        striped=True,
        highlightOnHover=True,
        withTableBorder=True,
        data={
            "head": [dictionary["teachers_concept"], dictionary["teachers_where"]],
            "body": [[dictionary[concept], dictionary[where]] for concept, where in CURRICULUM_ROWS],
        },
    )

    lesson_links = [
        _link_card(
            dictionary["ocean_title"],
            f"/ozean?lang={lang}",
            "mdi:image-filter-hdr",
        ),
        _link_card(
            dictionary["teachers_school_entry"],
            f"/?mode=schule&lang={lang}",
            "mdi:school-outline",
        ),
    ]
    lesson_links += [
        _link_card(
            preset.label[lang],
            f"/?{preset.settings.to_query()}&scen={preset.name}&mode=schule&lang={lang}",
            "mdi:earth",
        )
        for preset in SCHOOL_PRESETS
    ]
    lesson_links += [
        _link_card(
            experiment.label[lang],
            f"/?{experiment.disturbed.to_query()}&exp={experiment.name}&lang={lang}",
            "mdi:flask-outline",
        )
        for experiment in EXPERIMENTS
    ]

    tasks = dmc.List(
        [dmc.ListItem(dmc.Text(dictionary[key], size="sm"), mb=6) for key in TASK_KEYS],
        spacing="xs",
        type="ordered",
    )

    content = dmc.Stack(
        [
            dmc.Title(dictionary["teachers_title"], order=2),
            dmc.Text(dictionary["teachers_intro"], size="sm"),
            dmc.Divider(my=8),
            dmc.Title(dictionary["teachers_curriculum"], order=4),
            curriculum_table,
            dmc.Divider(my=8),
            dmc.Title(dictionary["teachers_lessons"], order=4),
            dmc.Box(lesson_links),
            dmc.Divider(my=8),
            dmc.Title(dictionary["teachers_tasks"], order=4),
            tasks,
            dmc.Divider(my=8),
            dmc.Alert(
                dmc.Text(dictionary["teachers_note"], size="sm"),
                title=dictionary["teachers_note_title"],
                color="gray",
                radius="md",
            ),
        ],
        gap="sm",
    )

    return dbc.Container(
        dbc.Row(dbc.Col(content, xs=12, lg=9, xl=7)),
        fluid=True,
        style={"paddingTop": "20px", "paddingBottom": "40px"},
    )
