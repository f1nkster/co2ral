# CO2RAL

Graphical user interface for exploring the marine carbon model of
[PyCO2SYS](https://pyco2sys.readthedocs.io/) — running at [co2ral.de](https://co2ral.de).

Built with [Plotly Dash](https://dash.plotly.com/) and
[Dash Mantine Components](https://www.dash-mantine-components.com/)
for the [Chair of Chemistry Education at FAU](https://www.chemiedidaktik.phil.fau.de/).

## Features

* Fix one carbonate system parameter (total alkalinity, DIC, pH or pCO₂) and vary a second
  one over a range; plot any of the other parameters (incl. CO₃²⁻, HCO₃⁻ and the
  aragonite/calcite saturation states Ω with a reference line at Ω = 1) against it
* Didactic scenario presets (ocean acidification, coral reef, North Sea, Baltic Sea)
* Guided Le Chatelier experiments and an optional Bjerrum plot with pK₁/pK₂ markers
* Explorer plots arranged in a draggable, resizable grid; the arrangement is remembered
  across live updates and page reloads (stacks to one column on phones)
* School mode (`?mode=schule`): reduced interface, everyday scenarios with guiding
  questions, plus a teacher page at `/lehrkraefte` with curriculum links and tasks
* Pictorial ocean view at `/ozean`: sky with CO₂ and water body with the resulting
  values, each shown as a change relative to 1850 — no chart reading required
* Particle model below the scene: the amounts hold while individual particles keep
  converting, showing that the equilibrium is dynamic
* Shareable urls: all settings are encoded as query parameters (copy via the share icon)
* Localized in German and English (`?lang=de` / `?lang=en`)
* Download plots as PNG including the fixed model conditions, or all results as CSV
  (German locale: semicolon separator and decimal comma for Excel)
* Responsive layout for tablets and phones
* All stylesheets and fonts are served locally (no CDN or Google Fonts requests)

## Open Points

* Nutrients to add: Ammonia: 0 - 1
* Live plot updates on slider changes (debounced)
* Bjerrum plot (carbonate speciation vs. pH)
* Selectable dissociation constants (opt_k_carbonic)
* Privacy: DashIconify loads icons from api.iconify.design at runtime; replace with
  bundled icons for a fully CDN-free page

