TRANSLATION_DICT: dict[str, dict[str, str]] = {
    "en": {
        "app_subtitle": "User Interface for Modeling Marine Carbon Systems",
        "basic_settings": "Basic Settings",
        "advanced_settings": "Advanced Settings",
        "model_settings": "Model Settings",
        "plot_settings": "Plot Settings",
        "fixed_parameter": "Fixed Parameter",
        "fixed_parameter_description": "Parameter which is fixed to a single value for the marine model.",
        "x_axis_parameter": "X-Axis",
        "x_axis_parameter_description": "Parameter representing the values for the x-axis.",
        "x_axis_settings": "X-Axis Settings",
        "x_min_label": "Min Value",
        "x_max_label": "Max Value",
        "num_points": "Number of Data Points",
        "y_axis_parameter": "Y-Axis",
        "y_axis_parameter_description": "Choose the parameters for the Y-Axis which creates the plots.",
        "apply_btn": "Apply",
        "reset_btn": "Reset",
        "imprint": "Imprint",
        "hydrographic_conditions": "Hydrographic Conditions",
        "practical_salinity": "Practical Salinity",
        "temperature": "Temperature",
        "nutrients": "Nutrients",
        "total_silicate": "Total Silicate",
        "total_phosphate": "Total Phosphate",
        "unit": "Unit",
        "plot_title_prefix": "Plot for ",
        "total_alkalinity": "Total Alkalinity",
        "scenarios": "Scenarios",
        "scenario_placeholder": "Choose a scenario …",
        "share_link": "Copy chart link",
        "download_csv": "Download data as CSV",
        "no_yaxis_warning": "Please select at least one y-axis parameter to create plots.",
        "context_fixed": "Fixed",
        "omega_hint": "Ω > 1: calcification possible · Ω < 1: calcium carbonate dissolves",
        "speciation_title": "DIC speciation",
        "speciation_hint": "Share of CO₂(aq), HCO₃⁻ and CO₃²⁻ in dissolved inorganic carbon — watch the equilibrium shift",
        "compare_start": "Save current state for comparison",
        "compare_stop": "End comparison",
        "comparison_suffix": " (comparison)",
        "comparison_prefix": "Comparison",
        "bjerrum_toggle": "Show Bjerrum plot",
        "bjerrum_title": "Bjerrum plot",
        "bjerrum_hint": (
            "Shares of the DIC species as a function of pH at the current temperature and salinity. "
            "The crossing points mark pK₁ and pK₂; dashed gray: pH range of the current model run."
        ),
        "fraction_label": "Fraction [%]",
        "current_ph_label": "current pH",
        "experiments": "Le Chatelier experiments",
        "experiments_hint": "Guided disturbances: the previous state stays visible as a gray comparison line.",
        "exp_end": "End experiment",
        "expl_alkalinity": (
            "Total alkalinity describes the seawater's capacity to neutralize acids (buffering capacity). "
            "It increases e.g. through weathering of carbonate rock."
        ),
        "expl_dic": (
            "DIC (dissolved inorganic carbon) is the sum of all inorganic carbon species in the water: "
            "CO₂, HCO₃⁻ and CO₃²⁻."
        ),
        "expl_pH": (
            "The pH value indicates how acidic or basic the water is. "
            "Today's surface seawater is at about 8.1 and is slowly decreasing (ocean acidification)."
        ),
        "expl_pCO2": (
            "The CO₂ partial pressure describes how much CO₂ is dissolved in the water — "
            "in equilibrium with the atmosphere (today ≈ 420 μatm, pre-industrial ≈ 280 μatm)."
        ),
        "expl_salinity": (
            "The practical salinity indicates the salt content of the water "
            "(open ocean ≈ 35, Baltic Sea ≈ 8, unitless)."
        ),
        "expl_temperature": (
            "Water temperature affects the solubility of CO₂: cold water can take up more CO₂ than warm water."
        ),
        "expl_total_silicate": (
            "Dissolved silicate is a nutrient and contributes slightly to the alkalinity of seawater."
        ),
        "expl_total_phosphate": (
            "Dissolved phosphate is a nutrient and contributes slightly to the alkalinity of seawater."
        ),
    },
    "de": {
        "app_subtitle": "Benutzeroberfläche zur Modellierung mariner Kohlenstoffsysteme",
        "model_settings": "Modelleinstellungen",
        "plot_settings": "Diagrammeinstellungen",
        "basic_settings": "Grundeinstellungen",
        "advanced_settings": "Erweiterte Einstellungen",
        "fixed_parameter": "Fester Parameter",
        "fixed_parameter_description": "Parameter, der für das marine Modell auf einen einzelnen Wert festgelegt ist.",
        "x_axis_parameter": "X-Achse",
        "x_axis_parameter_description": "Parameter, der die Werte für die x-Achse darstellt.",
        "x_axis_settings": "X-Achsen Einstellungen",
        "x_min_label": "Min Wert",
        "x_max_label": "Max Wert",
        "num_points": "Anzahl Datenpunkte",
        "y_axis_parameter": "Y-Achse",
        "y_axis_parameter_description": "Wähle Parameter für die Y-Achse, die in einzelnen Diagrammen dargestellt werden.",
        "apply_btn": "Los geht's",
        "reset_btn": "Reset",
        "imprint": "Impressum",
        "hydrographic_conditions": "Hydrographische Bedingungen",
        "practical_salinity": "Praktische Salinität",
        "temperature": "Temperatur",
        "nutrients": "Mineralien",
        "total_silicate": "Totales Silikat",
        "total_phosphate": "Totales Phosphat",
        "unit": "Einheit",
        "plot_title_prefix": "Diagramm für ",
        "total_alkalinity": "Gesamtalkalität",
        "scenarios": "Szenarien",
        "scenario_placeholder": "Szenario auswählen …",
        "share_link": "Diagramm-Link kopieren",
        "download_csv": "Daten als CSV herunterladen",
        "no_yaxis_warning": "Bitte wähle mindestens einen Y-Achsen-Parameter aus, um Diagramme zu erstellen.",
        "context_fixed": "Fest",
        "omega_hint": "Ω > 1: Kalkbildung möglich · Ω < 1: Kalk löst sich auf",
        "speciation_title": "Speziesverteilung im DIC",
        "speciation_hint": "Anteile von CO₂(aq), HCO₃⁻ und CO₃²⁻ am gelösten anorganischen Kohlenstoff — beobachte, wie sich das Gleichgewicht verschiebt",
        "compare_start": "Aktuellen Zustand für Vergleich merken",
        "compare_stop": "Vergleich beenden",
        "comparison_suffix": " (Vergleich)",
        "comparison_prefix": "Vergleich",
        "bjerrum_toggle": "Bjerrum-Diagramm anzeigen",
        "bjerrum_title": "Bjerrum-Diagramm",
        "bjerrum_hint": (
            "Anteile der DIC-Spezies in Abhängigkeit vom pH bei aktueller Temperatur und Salinität. "
            "Die Schnittpunkte markieren pK₁ und pK₂; grau gestrichelt: pH-Bereich des aktuellen Modelllaufs."
        ),
        "fraction_label": "Anteil [%]",
        "current_ph_label": "aktueller pH",
        "experiments": "Le-Chatelier-Experimente",
        "experiments_hint": "Geführte Störungen: Der vorherige Zustand bleibt als graue Vergleichslinie sichtbar.",
        "exp_end": "Experiment beenden",
        "expl_alkalinity": (
            "Die Gesamtalkalität beschreibt die Fähigkeit des Meerwassers, Säuren zu neutralisieren "
            "(Puffervermögen). Sie steigt z. B. durch Verwitterung von Kalkgestein."
        ),
        "expl_dic": (
            "DIC (gelöster anorganischer Kohlenstoff) ist die Summe aller anorganischen "
            "Kohlenstoffspezies im Wasser: CO₂, HCO₃⁻ und CO₃²⁻."
        ),
        "expl_pH": (
            "Der pH-Wert gibt an, wie sauer oder basisch das Wasser ist. "
            "Oberflächen-Meerwasser liegt heute bei etwa 8,1 und sinkt langsam (Ozeanversauerung)."
        ),
        "expl_pCO2": (
            "Der CO₂-Partialdruck beschreibt, wie viel CO₂ im Wasser gelöst ist — "
            "im Gleichgewicht mit der Atmosphäre (heute ≈ 420 μatm, vorindustriell ≈ 280 μatm)."
        ),
        "expl_salinity": (
            "Die praktische Salinität gibt den Salzgehalt des Wassers an "
            "(offener Ozean ≈ 35, Ostsee ≈ 8, einheitenlos)."
        ),
        "expl_temperature": (
            "Die Wassertemperatur beeinflusst die Löslichkeit von CO₂: "
            "Kaltes Wasser kann mehr CO₂ aufnehmen als warmes."
        ),
        "expl_total_silicate": (
            "Gelöstes Silikat ist ein Nährstoff und trägt geringfügig zur Alkalität des Meerwassers bei."
        ),
        "expl_total_phosphate": (
            "Gelöstes Phosphat ist ein Nährstoff und trägt geringfügig zur Alkalität des Meerwassers bei."
        ),
    },
}
