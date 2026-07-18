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
* Shareable urls: all settings are encoded as query parameters (copy via the share icon)
* Localized in German and English (`?lang=de` / `?lang=en`)
* Download plots as PNG including the fixed model conditions, or all results as CSV
  (German locale: semicolon separator and decimal comma for Excel)
* Responsive layout for tablets and phones
* All stylesheets and fonts are served locally (no CDN or Google Fonts requests)

## Development

```bash
poetry install
cd co2ral
poetry run python serve.py   # production server (waitress) on http://127.0.0.1:8050
poetry run python __main__.py --debug   # dev server with debug mode
```

Run tests and linting:

```bash
poetry run pytest
poetry run ruff check co2ral tests
poetry run ruff format --check co2ral tests
```

## Open Points

* Nutrients to add: Ammonia: 0 - 1
* Live plot updates on slider changes (debounced)
* Bjerrum plot (carbonate speciation vs. pH)
* Selectable dissociation constants (opt_k_carbonic)
* Privacy: DashIconify loads icons from api.iconify.design at runtime; replace with
  bundled icons for a fully CDN-free page

# Deployment

CO2RAL is using waitress for the WSGI app and nginx for the webserver.
Linux service is defined in /etc/systemd/system/co2ral.service

How to check the status: ```sudo systemctl status co2ral```
How to stop: ```sudo systemctl stop co2ral```
How to start: ```sudo systemctl start co2ral```
Show logs: ```sudo journalctl -u co2ral```

Deploy a new version:

```bash
cd /home/heiter/co2ral
sudo -u heiter git pull
sudo systemctl restart co2ral
```

# Certificates for SSL

Mainly, we are using certbot for that:
```
sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d co2ral.de -d www.co2ral.de
```
