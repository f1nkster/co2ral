from dataclasses import dataclass

import dash_mantine_components as dmc
from core.utils.marine_model import run_single_state
from dash import html
from dash.development.base_component import Component
from locales.translation import TRANSLATION_DICT


# Number of particles drawn. Enough to show the proportions, few enough to stay countable.
PARTICLE_TOTAL = 40

# Duration of one full conversion cycle in seconds; partners run half a cycle out of phase,
# so at every moment one particle of each species exists in a pair.
SWAP_SECONDS = 8

# Species colours taken from the design project, matching the speciation chart.
SPECIES_COLORS = {"CO2": "#eab308", "HCO3": "#0ea5e9", "CO3": "#7c3aed"}
SPECIES_LABELS = {"CO2": "CO₂", "HCO3": "HCO₃⁻", "CO3": "CO₃²⁻"}
SPECIES_ORDER = ("CO2", "HCO3", "CO3")


@dataclass
class Particle:
    """One drawn particle: either a fixed species or one half of a converting pair."""

    species: str
    partner_species: str | None = None
    second_phase: bool = False


def _particle_counts(state: dict[str, float]) -> dict[str, int]:
    """Distributes the drawn particles over the three species according to their real shares.

    Every species gets at least one particle, so the rare CO2 stays visible and the
    conversion can be shown at all.

    :param state: Result of a single model state.
    :return: Particle count per species, summing to PARTICLE_TOTAL.
    """
    total = sum(state[species] for species in SPECIES_ORDER)
    counts = {species: max(1, round(state[species] / total * PARTICLE_TOTAL)) for species in SPECIES_ORDER}

    # HCO3 dominates by far, so it absorbs the rounding difference.
    counts["HCO3"] = max(1, PARTICLE_TOTAL - counts["CO2"] - counts["CO3"])
    return counts


def _build_particles(counts: dict[str, int]) -> list[Particle]:
    """Builds the particle list, turning some of them into converting pairs.

    A pair always shows one particle of each of its two species, so the totals stay
    constant while the individual particles keep changing identity.

    :param counts: Particle count per species.
    :return: Particle descriptors in a spread-out order.
    """
    # One CO2 <-> HCO3 pair (the first equilibrium) and up to two HCO3 <-> CO3 pairs.
    pairs_carbonic = 1 if counts["CO2"] >= 1 and counts["HCO3"] >= 2 else 0
    pairs_carbonate = min(2, counts["CO3"], max(0, counts["HCO3"] - pairs_carbonic - 1))

    particles: list[Particle] = []
    for _ in range(pairs_carbonic):
        particles.append(Particle(species="CO2", partner_species="HCO3", second_phase=False))
        particles.append(Particle(species="HCO3", partner_species="CO2", second_phase=True))
    for _ in range(pairs_carbonate):
        particles.append(Particle(species="HCO3", partner_species="CO3", second_phase=False))
        particles.append(Particle(species="CO3", partner_species="HCO3", second_phase=True))

    static_counts = {
        "CO2": counts["CO2"] - pairs_carbonic,
        "HCO3": counts["HCO3"] - pairs_carbonic - pairs_carbonate,
        "CO3": counts["CO3"] - pairs_carbonate,
    }
    for species in SPECIES_ORDER:
        particles.extend(Particle(species=species) for _ in range(max(0, static_counts[species])))

    # Spread the species over the box instead of drawing them in blocks.
    count = len(particles)
    order = sorted(range(count), key=lambda index: (index * 13) % count)
    return [particles[index] for index in order]


def _position(index: int) -> tuple[float, float]:
    """Places a particle on a jittered grid, deterministically.

    :param index: Position of the particle in the list.
    :return: Tuple of left and top in percent.
    """
    columns = 8
    column, row = index % columns, index // columns
    jitter_left = ((index * 7) % 5) - 2
    jitter_top = ((index * 11) % 5) - 2
    return (4 + column * 11.8 + jitter_left, 8 + row * 17 + jitter_top)


def _face(species: str, class_name: str, delay: str) -> Component:
    """One visible side of a converting particle.

    :param species: Species shown on this face.
    :param class_name: Face class carrying the crossfade animation.
    :param delay: CSS animation delay, used to flip a partner into the opposite phase.
    :return: Face component.
    """
    return html.Div(
        SPECIES_LABELS[species],
        className=f"particle-face {class_name}",
        style={"backgroundColor": SPECIES_COLORS[species], "animationDelay": delay},
    )


def _render_particle(particle: Particle, index: int) -> Component:
    """Renders a single particle at its grid position.

    :param particle: The particle descriptor.
    :param index: Position in the list, used for placement and animation variation.
    :return: Particle component.
    """
    left, top = _position(index)
    style = {
        "left": f"{left}%",
        "top": f"{top}%",
        # Vary drift so the particles do not move in lockstep.
        "animationDuration": f"{12 + (index % 5) * 2}s",
        "animationDelay": f"-{(index % 7) * 1.5}s",
    }

    if particle.partner_species is None:
        return html.Div(
            SPECIES_LABELS[particle.species],
            className="particle",
            style={**style, "backgroundColor": SPECIES_COLORS[particle.species]},
        )

    # Converting particle: two crossfading faces. The partner runs half a cycle later,
    # so the pair always shows one particle of each species.
    delay = f"-{SWAP_SECONDS / 2}s" if particle.second_phase else "0s"
    return html.Div(
        [
            _face(particle.species, "particle-face-a", delay),
            _face(particle.partner_species, "particle-face-b", delay),
        ],
        className="particle particle-swap",
        style=style,
    )


def create_particle_view(value_pco2: float, value_temperature: float, lang: str = "de") -> Component:
    """Builds the particle model of the current seawater state.

    The particle counts follow the real speciation, while a few particles keep converting
    into one another — showing that the equilibrium is dynamic although the amounts hold.

    :param value_pco2: CO2 partial pressure in the air, in μatm.
    :param value_temperature: Water temperature in °C.
    :param lang: Selected language.
    :return: The particle box with legend and counts.
    """
    dictionary = TRANSLATION_DICT[lang]
    state = run_single_state(value_pco2=value_pco2, value_temperature=value_temperature)
    counts = _particle_counts(state)
    particles = _build_particles(counts)

    total_concentration = sum(state[species] for species in SPECIES_ORDER)
    shares = {species: state[species] / total_concentration * 100 for species in SPECIES_ORDER}

    box = html.Div(
        [_render_particle(particle, index) for index, particle in enumerate(particles)],
        className="particle-box",
    )

    legend = dmc.Group(
        [
            dmc.Group(
                [
                    html.Div(
                        className="particle-dot",
                        style={"backgroundColor": SPECIES_COLORS[species]},
                    ),
                    dmc.Text(
                        f"{SPECIES_LABELS[species]}: {counts[species]}",
                        size="xs",
                        fw=600,
                    ),
                    dmc.Text(f"({shares[species]:.1f} %)", size="xs", c="dimmed"),
                ],
                gap=4,
            )
            for species in SPECIES_ORDER
        ],
        gap="md",
        mt="xs",
    )

    return dmc.Paper(
        [
            dmc.Title(dictionary["particles_title"], order=4),
            dmc.Text(dictionary["particles_intro"], size="sm", mt=4),
            box,
            legend,
            dmc.Alert(dmc.Text(dictionary["particles_note"], size="sm"), color="teal", radius="md", mt="sm"),
            dmc.Text(dictionary["particles_min_note"], size="xs", c="dimmed", mt=4),
        ],
        p="md",
        radius="md",
        withBorder=True,
        mt="md",
    )
