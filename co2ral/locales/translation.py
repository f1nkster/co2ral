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
        "nav_home": "Explorer",
        "nav_teachers": "For teachers",
        "footer_credit": (
            "All calculations on this site are performed by PyCO2SYS, an open-source Python "
            "implementation of the marine carbonate system by Humphreys et al."
        ),
        "footer_repo": "PyCO2SYS on GitHub",
        "footer_docs": "PyCO2SYS documentation",
        "footer_source": "CO2RAL source code",
        "school_scenarios": "Choose a topic",
        "school_explore": "Try it out",
        "nav_ocean": "Ocean view",
        "ocean_title": "What does CO₂ do to the ocean?",
        "ocean_intro": (
            "Move the two sliders and watch what changes in the water. "
            "All values are calculated for a typical patch of ocean surface."
        ),
        "ocean_atmosphere": "Air above the sea",
        "ocean_water": "In the seawater",
        "ocean_co2_slider": "CO₂ in the air",
        "ocean_temp_slider": "Water temperature",
        "ocean_vs_1850": "compared to 1850",
        "ocean_ph": "Acidity (pH)",
        "ocean_ph_note": "lower = more acidic",
        "ocean_omega": "Carbonate saturation (Ω aragonite)",
        "ocean_co2_aq": "Dissolved CO₂",
        "ocean_hco3": "Hydrogen carbonate HCO₃⁻",
        "ocean_co3": "Carbonate CO₃²⁻",
        "ocean_dic": "Total dissolved carbon (DIC)",
        "ocean_coral_good": "Corals and shells can build their calcium carbonate well.",
        "ocean_coral_hard": "It is getting harder for corals to build their calcium carbonate.",
        "ocean_coral_bad": "Calcium carbonate dissolves — shells and coral skeletons are attacked.",
        "ocean_hint_ph": "The pH scale is logarithmic: 0.3 less pH means about twice as many H⁺ ions.",
        "ocean_back": "Back to the charts",
        "ocean_1850": "1850",
        "ocean_today": "today",
        "ocean_2100": "possible 2100",
        "ocean_jump": "Jump to:",
        "school_intro": "Pick a topic, then explore: drag the temperature slider and watch the charts respond.",
        "school_question": "Question",
        "to_school_mode": "School mode",
        "to_pro_mode": "Full mode",
        "teachers_title": "CO2RAL for teaching",
        "teachers_intro": (
            "CO2RAL models the marine carbonate system — a real-world context that covers the whole "
            "curriculum area of chemical equilibrium. Every link below opens a ready-to-use state of the "
            "app; copy it into your worksheet or learning platform."
        ),
        "teachers_curriculum": "Curriculum links",
        "teachers_concept": "Concept",
        "teachers_where": "Where in CO2RAL",
        "teachers_lessons": "Ready-made lesson links",
        "teachers_tasks": "Task suggestions",
        "teachers_school_entry": "School mode (reduced interface)",
        "teachers_note_title": "Good to know",
        "teachers_note": (
            "All settings are stored in the url, so any state you build can be shared as a link. "
            "Charts can be downloaded as PNG, the underlying values as CSV (semicolon and decimal comma "
            "in the German version, opens directly in Excel)."
        ),
        "curr_dynamic": "Equilibrium as a dynamic state",
        "curr_dynamic_where": (
            "Ocean view and speciation panel: the shares shift while the system stays in equilibrium"
        ),
        "curr_lechatelier": "Le Chatelier: concentration and temperature",
        "curr_lechatelier_where": "Guided experiments: CO₂ input, warming, adding lime",
        "curr_acidbase": "Acid-base equilibria, pK values",
        "curr_acidbase_where": "Bjerrum plot with pK₁ and pK₂ markers",
        "curr_solubility": "Solubility equilibrium",
        "curr_solubility_where": "Saturation states Ω with the Ω = 1 threshold",
        "curr_buffer": "Buffer systems",
        "curr_buffer_where": "Buffer experiment: seawater vs. low-alkalinity water",
        "task_1": (
            "Read off the pH for 280, 420 and 1000 μatm pCO₂ and calculate the difference. "
            "Note: the pH scale is logarithmic — what does a drop of 0.3 mean for the H⁺ concentration?"
        ),
        "task_2": (
            "In the speciation panel, describe how the shares of CO₂(aq), HCO₃⁻ and CO₃²⁻ change as CO₂ rises. "
            "Which species dominates in seawater, and why?"
        ),
        "task_3": (
            "Determine from the Ω plot the pCO₂ at which Ω drops below 1, and explain what this means "
            "for corals and shellfish."
        ),
        "task_4": (
            "Compare the ocean and Baltic Sea scenarios: explain, using alkalinity, why the same CO₂ increase "
            "changes the pH differently."
        ),
        "task_5": (
            "Use the warming experiment to explain, with Le Chatelier's principle, why warm water holds less CO₂."
        ),
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
        "nav_home": "Explorer",
        "nav_teachers": "Für Lehrkräfte",
        "footer_credit": (
            "Alle Berechnungen dieser Seite führt PyCO2SYS durch — eine freie Python-Umsetzung "
            "des marinen Karbonatsystems von Humphreys et al."
        ),
        "footer_repo": "PyCO2SYS auf GitHub",
        "footer_docs": "PyCO2SYS-Dokumentation",
        "footer_source": "Quellcode von CO2RAL",
        "school_scenarios": "Wähle ein Thema",
        "school_explore": "Ausprobieren",
        "nav_ocean": "Ozean-Ansicht",
        "ocean_title": "Was macht CO₂ mit dem Meer?",
        "ocean_intro": (
            "Bewege die beiden Regler und beobachte, was sich im Wasser verändert. "
            "Alle Werte gelten für ein typisches Stück Meeresoberfläche."
        ),
        "ocean_atmosphere": "Luft über dem Meer",
        "ocean_water": "Im Meerwasser",
        "ocean_co2_slider": "CO₂ in der Luft",
        "ocean_temp_slider": "Wassertemperatur",
        "ocean_vs_1850": "gegenüber 1850",
        "ocean_ph": "Säuregrad (pH)",
        "ocean_ph_note": "kleiner = saurer",
        "ocean_omega": "Kalk-Sättigung (Ω Aragonit)",
        "ocean_co2_aq": "Gelöstes CO₂",
        "ocean_hco3": "Hydrogencarbonat HCO₃⁻",
        "ocean_co3": "Carbonat CO₃²⁻",
        "ocean_dic": "Gelöster Kohlenstoff gesamt (DIC)",
        "ocean_coral_good": "Korallen und Muscheln können ihren Kalk gut aufbauen.",
        "ocean_coral_hard": "Für Korallen wird es schwieriger, Kalk aufzubauen.",
        "ocean_coral_bad": "Kalk löst sich auf — Muschelschalen und Korallenskelette werden angegriffen.",
        "ocean_hint_ph": "Die pH-Skala ist logarithmisch: 0,3 weniger pH bedeutet etwa doppelt so viele H⁺-Ionen.",
        "ocean_back": "Zurück zu den Diagrammen",
        "ocean_1850": "1850",
        "ocean_today": "heute",
        "ocean_2100": "mögliche 2100",
        "ocean_jump": "Springe zu:",
        "school_intro": "Wähle ein Thema und probiere aus: Zieh am Temperaturregler und beobachte die Diagramme.",
        "school_question": "Frage",
        "to_school_mode": "Schulmodus",
        "to_pro_mode": "Vollmodus",
        "teachers_title": "CO2RAL im Unterricht",
        "teachers_intro": (
            "CO2RAL modelliert das marine Karbonatsystem — ein realer Kontext, der den gesamten Lehrplanbereich "
            "des chemischen Gleichgewichts abdeckt. Jeder Link unten öffnet einen fertigen Zustand der App; "
            "kopiere ihn in dein Arbeitsblatt oder deine Lernplattform."
        ),
        "teachers_curriculum": "Lehrplanbezug",
        "teachers_concept": "Konzept",
        "teachers_where": "Wo in CO2RAL",
        "teachers_lessons": "Fertige Unterrichts-Links",
        "teachers_tasks": "Aufgabenvorschläge",
        "teachers_school_entry": "Schulmodus (reduzierte Oberfläche)",
        "teachers_note_title": "Gut zu wissen",
        "teachers_note": (
            "Alle Einstellungen stecken in der URL — jeder selbst gebaute Zustand lässt sich als Link weitergeben. "
            "Diagramme können als PNG heruntergeladen werden, die zugrunde liegenden Werte als CSV "
            "(Semikolon und Dezimalkomma in der deutschen Version, öffnet direkt in Excel)."
        ),
        "curr_dynamic": "Gleichgewicht als dynamischer Zustand",
        "curr_dynamic_where": (
            "Ozean-Ansicht und Speziesverteilung: Die Anteile verschieben sich, das System bleibt im Gleichgewicht"
        ),
        "curr_lechatelier": "Le Chatelier: Konzentration und Temperatur",
        "curr_lechatelier_where": "Geführte Experimente: CO₂-Eintrag, Erwärmung, Kalkzugabe",
        "curr_acidbase": "Säure-Base-Gleichgewichte, pK-Werte",
        "curr_acidbase_where": "Bjerrum-Diagramm mit pK₁- und pK₂-Markern",
        "curr_solubility": "Löslichkeitsgleichgewicht",
        "curr_solubility_where": "Sättigungszustände Ω mit der Schwelle Ω = 1",
        "curr_buffer": "Puffersysteme",
        "curr_buffer_where": "Puffer-Experiment: Meerwasser vs. alkalinitätsarmes Wasser",
        "task_1": (
            "Lies den pH-Wert für 280, 420 und 1000 μatm pCO₂ ab und berechne die Differenz. "
            "Beachte: Die pH-Skala ist logarithmisch — was bedeutet ein Abfall um 0,3 für die H⁺-Konzentration?"
        ),
        "task_2": (
            "Beschreibe anhand der Speziesverteilung, wie sich die Anteile von CO₂(aq), HCO₃⁻ und CO₃²⁻ bei "
            "steigendem CO₂ verändern. Welche Spezies überwiegt im Meerwasser, und warum?"
        ),
        "task_3": (
            "Bestimme aus dem Ω-Diagramm den pCO₂-Wert, bei dem Ω unter 1 fällt, und erkläre, was das für "
            "Korallen und Muscheln bedeutet."
        ),
        "task_4": (
            "Vergleiche die Szenarien Ozean und Ostsee: Erkläre mithilfe der Alkalinität, warum derselbe "
            "CO₂-Anstieg den pH unterschiedlich stark verändert."
        ),
        "task_5": (
            "Erkläre mit dem Prinzip von Le Chatelier anhand des Erwärmungs-Experiments, warum warmes Wasser "
            "weniger CO₂ aufnehmen kann."
        ),
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
