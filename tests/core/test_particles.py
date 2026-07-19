from collections import Counter

from core.utils.marine_model import run_single_state
from core.utils.particles import (
    PARTICLE_TOTAL,
    SPECIES_ORDER,
    _build_particles,
    _particle_counts,
    create_particle_view,
)


def _collect_text(component) -> str:
    """Collects all text contained in a dash component tree.

    :param component: Component or primitive to walk.
    :return: Concatenated text of the whole tree.
    """
    if component is None:
        return ""
    if isinstance(component, str | int | float):
        return str(component)
    if isinstance(component, list | tuple):
        return " ".join(_collect_text(item) for item in component)

    text = ""
    for attribute in ("children", "label", "title"):
        if hasattr(component, attribute):
            text += " " + _collect_text(getattr(component, attribute))
    return text


def test__particle_counts__sum_to_total_and_keep_every_species_visible():
    """GIVEN a present-day seawater state
    WHEN the particle counts are derived
    THEN they sum to the drawn total and no species disappears, even the very rare CO2
    """
    counts = _particle_counts(run_single_state(value_pco2=420, value_temperature=18))

    assert sum(counts.values()) == PARTICLE_TOTAL
    assert all(counts[species] >= 1 for species in SPECIES_ORDER)
    # Hydrogen carbonate dominates the carbonate system by far.
    assert counts["HCO3"] > counts["CO3"] > counts["CO2"]


def test__build_particles__pairs_preserve_the_species_totals():
    """GIVEN particle counts
    WHEN the particles are built with converting pairs
    THEN each pair contributes one particle of each of its two species, so the totals
         match the counts at every moment of the animation
    """
    counts = _particle_counts(run_single_state(value_pco2=420, value_temperature=18))
    particles = _build_particles(counts)

    assert len(particles) == PARTICLE_TOTAL
    # The species currently shown, i.e. the first half of every swap cycle.
    shown = Counter(particle.species for particle in particles)
    assert shown == Counter(counts)

    # After half a cycle each pair shows its partner instead; the totals must not change.
    swapped = Counter(particle.partner_species or particle.species for particle in particles)
    assert swapped == Counter(counts)


def test__build_particles__contains_converting_pairs():
    """GIVEN a typical seawater state
    WHEN the particles are built
    THEN at least one pair actually converts, otherwise the dynamic equilibrium
         would not be visible at all
    """
    counts = _particle_counts(run_single_state(value_pco2=420, value_temperature=18))
    particles = _build_particles(counts)

    converting = [particle for particle in particles if particle.partner_species is not None]

    assert len(converting) >= 2
    assert len(converting) % 2 == 0, "converting particles must come in pairs"
    assert any(particle.second_phase for particle in converting)


def test__particle_counts__shift_towards_co2_when_co2_rises():
    """GIVEN a low and a high CO2 level
    WHEN the particle counts are derived for both
    THEN the carbonate share shrinks as CO2 rises, mirroring the equilibrium shift
    """
    low = _particle_counts(run_single_state(value_pco2=280, value_temperature=18))
    high = _particle_counts(run_single_state(value_pco2=1100, value_temperature=18))

    assert high["CO3"] < low["CO3"]


def test__create_particle_view__shows_counts_and_the_equilibrium_message():
    """GIVEN a seawater state
    WHEN the particle view is built
    THEN it names all three species and explains that the amounts stay constant
    """
    text = _collect_text(create_particle_view(value_pco2=420, value_temperature=18, lang="de"))

    assert "CO₂" in text and "HCO₃⁻" in text and "CO₃²⁻" in text
    assert "dynamisches Gleichgewicht" in text
