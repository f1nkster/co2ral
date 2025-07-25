## ToDos
* Integrierte GUI oder Webserver (Dash App)?
* Wenn Dash App - welcher Server verfügbar? SQL Datenbanken (für Cache)?
* Caching
* genaue Zielgruppe der Nutzer
    * Oberstufe
* alle Parameter relevant?

20.12.2024
* mehrere Parameter hinzufügen (customizable)
* Hauptparameter:
    Total alkalinity (type 1) in μmol·kg−1.
    Dissolved inorganic carbon (type 2) in μmol·kg−1.
    pH (type 3) on the Total, Seawater, Free or NBS scale1. Which scale is given by the argument opt_pH_scale.
*  Partial pressure of CO2
* Carbonate ion
* Bicarbonate ion
* @Shielyboi: Parametergrenzen überdenken
* v1.0 exe zuschicken

26.01.2025
* Aufwandsabschätzung für Werk (Spezifikationen - Minimal Valuable Product)
    - 40h mit 75€ = 3000€
* nächstes Meeting
    - Schätzung
    - weitere Stand des UI

10.02.2025
* chemische Spezien mit tiefgestellten Indices, hochgestellte Ladung
* Customfunktion von Plots, Plots save as JPG
* Extraktionsfunktion CSV
* URL soll sharable (stateless)
* Werteskalen
    * Alkalinity: 2000 - 2500
    * Salinität: 0-50
    * Silicate: 0-100
    * Silicate: 0-100
    * Phosphate: 0 - 5
* Nutrients to add
    * Ammonia: 0 - 1
* alle chemischen Spezien als Output plot im Output Accordion
* Advanced Settings:
    * Gleichgewichtskonstanten
* Future ideas- jmol integration

18.07.2025
* Reset Button
* pH Wert als Parameter, DIC(pH, pCO)
* Impressum der Uni direkt verlinken
* mehr Datenpunkte


# Deployment
CO2RAL is using waitress for the WSGI app and nginx for the webserver.
Linux service is defined in /etc/systemd/system/co2ral.service