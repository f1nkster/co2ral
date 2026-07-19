# CO2RAL Roadmap

Ziel: CO2RAL vom Karbonatsystem-Explorer zum Lernwerkzeug für **dynamische chemische
Gleichgewichte** ausbauen — nutzbar in Hochschule **und Schule (Sek II, perspektivisch Sek I)**.

Das Karbonatsystem eignet sich dafür ideal, weil es alle Lehrplan-Kernideen zum
chemischen Gleichgewicht in einem realen Kontext vereint:

| Lehrplan-Konzept | Im Karbonatsystem |
|---|---|
| Gleichgewicht als dynamischer Zustand | CO₂(g) ⇌ CO₂(aq) ⇌ HCO₃⁻ ⇌ CO₃²⁻ |
| Le Chatelier: Konzentration | CO₂-Eintrag verschiebt die Kaskade (Ozeanversauerung) |
| Le Chatelier: Temperatur | Löslichkeit von CO₂, K1/K2 temperaturabhängig |
| Säure-Base-Gleichgewichte | zweiprotonige Kohlensäure, pH |
| Löslichkeitsgleichgewicht | CaCO₃, Sättigungszustand Ω |
| Puffersysteme | Alkalinität / warum der Ozean pH-stabil ist |

Effort-Angaben: **S** = klein (Stunden), **M** = mittel (1–2 Sessions), **L** = groß (mehrere Sessions).

---

## Phase 1 — Dynamik sichtbar machen

Fundament: Das Gleichgewicht soll *unmittelbar* auf Eingriffe reagieren.

- [x] **Live-Updates (S)** — Diagramme aktualisieren beim Loslassen der Slider, „Los geht's"
      bleibt als Fallback. Serverlast unkritisch (ms-Berechnungen, clientseitiges Rendering).
- [x] **Ergebnis-Cache (S)** — `lru_cache` um den Modellaufruf; die Eingaben sind diskret,
      im Unterricht rechnen alle dieselben Presets.
- [x] **Speziesverteilungs-Panel (M)** — 100-%-Flächendiagramm: Wie teilt sich DIC in
      CO₂(aq) / HCO₃⁻ / CO₃²⁻ auf? Reagiert live auf die Slider → *das Gleichgewicht
      verschiebt sich sichtbar*. CO₂(aq) ist zusätzlich als Y-Parameter wählbar.
- [x] **Vergleichsmodus vorher/nachher (M)** — Zustand „einfrieren", dann stören:
      beide Kurven überlagert in einem Diagramm, beide Parametersätze im Untertitel
      dokumentiert. Kernwerkzeug für „Störung → Antwort des Gleichgewichts".

## Phase 2 — Gleichgewichte verstehen

- [x] **Bjerrum-Diagramm (M)** — das klassische Speziierungsdiagramm (Anteile vs. pH),
      zuschaltbar, mit pK₁/pK₂-Markern an den Kurvenschnittpunkten und Markierung des
      pH-Bereichs des aktuellen Laufs; Kurvenlage abhängig von T und S.
- [x] **Le-Chatelier-Experimente (M)** — vier geführte Störungen mit Erklär-Banner:
      CO₂-Eintrag, Erwärmung, Kalkzugabe, Puffervergleich. Jeweils gestörter Zustand
      gegen eingefrorene Baseline als Vergleichsserie; per URL teilbar (exp=…).
- [x] **Puffer erleben (S)** — als Experiment „Meerwasser vs. alkalinitätsarmes Wasser":
      gleicher CO₂-Anstieg, drastisch anderer pH-Effekt → Alkalinität als Puffer begreifen.

## Phase 3 — Schultauglichkeit

- [x] **Schulmodus (M)** — eigener Einstieg über `?mode=schule`: reduzierte Oberfläche
      (Themenwahl + Temperaturregler sichtbar, technische Steuerung ausgeblendet — alle
      Komponenten bleiben gemountet, weil die Callbacks ihre IDs brauchen), Sektion
      „Ausprobieren" standardmäßig offen, Moduswechsel per Link. Didaktische Reduktion
      statt Feature-Abbau; der Modus bleibt bei Reset, Sprachwechsel und Teilen erhalten.
- [x] **Alltags-Szenarien (S)** — vier Themen mit Leitfrage in einfacher Sprache:
      „Der Ozean: früher, heute, morgen", „Warmes Meer, kaltes Meer", „Korallen in Gefahr",
      „Ostsee: empfindlicher als der Ozean?". Die Leitfrage erscheint als Banner über den
      Diagrammen (`scen=`-Parameter).
- [x] **Materialseite für Lehrkräfte (M)** — eigene Seite `/lehrkraefte` mit
      Lehrplanbezugs-Tabelle (Konzept → wo in CO2RAL), fertigen Unterrichts-Links
      (Schulmodus, alle Szenarien und Experimente), fünf Aufgabenvorschlägen und
      Hinweisen zu Teilen/Export; später Arbeitsblätter als PDF.
- [x] **Ozean-Ansicht (M)** — bildliche Darstellung statt Diagramm unter `/ozean`: Himmel mit
      CO₂-Menge und Dunst, Temperaturanzeige, Wasserkörper mit den resultierenden Zahlenwerten
      (pH, Ω Aragonit, CO₂(aq), CO₃²⁻, HCO₃⁻, DIC). Jeder Wert zeigt zusätzlich die Änderung
      gegenüber 1850, sodass die Wirkung einer Reglerbewegung direkt ablesbar ist; darunter ein
      Klartext-Urteil zur Kalkbildung. Zwei Regler (CO₂, Temperatur), Sprungmarken 1850/heute/2100,
      Zustand über `?co2=&temp=` teilbar.
- [ ] **Aufgaben-/Lernpfadmodus (L)** — geführte Erkundungen in der App
      („Stelle pCO₂ auf 280 μatm. Beobachte Ω. Was bedeutet das für Korallen?") mit
      Schritt-Karten. Größtes Einzel-Feature, lohnt erst nach Phase 1+2.

## Phase 3.5 — Aktives Lernen

- [x] **Vorhersage-Modus (M)** — zuschaltbar (Schalter oder `?predict=1`): Nach jeder
      Reglerbewegung werden alle Wasserwerte verdeckt und eine Frage gestellt
      („Was passiert mit dem pH?"). Erst nach dem Tipp erscheinen die Werte, zusammen mit
      Rückmeldung und einer fachlichen Begründung. Der CO₂-Regler fragt nach dem pH,
      der Temperaturregler nach dem gelösten CO₂.
- [ ] **Selbstkontrolle mit erklärendem Feedback (M)** — eingebettete Verständnisfragen
      pro Szenario, Feedback verweist auf die passende Stelle im Bild.
- [ ] **Beobachtungs-Box (S)** — Lernende formulieren in einem Satz, was sie sehen;
      Export der eigenen Notizen als kleines Forschungsheft.
- [ ] **Brücke Bild → Diagramm (S)** — geführter Übergang von der Ozean-Ansicht zur Kurve.

## Phase 4 — Kür & Technik

- [x] **Teilchen-Animation „dynamisches Gleichgewicht" (L)** — Teilchenmodell unter der
      Ozean-Ansicht: 40 Teilchen im realen Mengenverhältnis von CO₂(aq), HCO₃⁻ und CO₃²⁻;
      einzelne Paare wandeln sich sichtbar ineinander um, laufen dabei aber gegenphasig,
      sodass die Anzahl jeder Sorte konstant bleibt — gegen die Fehlvorstellung
      „im Gleichgewicht passiert nichts".
- [ ] **Icons lokal bündeln (S)** — DashIconify lädt zur Laufzeit von api.iconify.design;
      letzter externer Request (Datenschutz).
- [ ] **Datenschutzerklärung (S)** — eigene Seite; für Schuleinsatz relevant.
- [ ] **Wählbare Konstanten opt_k_carbonic (S)** — Hochschul-Feature, im Code vorbereitet.
- [ ] **Ammonium als Nährstoff (S)** — offener Punkt aus der Ursprungsversion.
- [ ] **Achsen-Umschalter „ab Null" (S)** — für Diskussionen über Darstellung/Manipulation
      von Diagrammen (nebenbei selbst ein Lernziel).

---

## Leitplanken

- **Einfachheit schlägt Featurezahl:** Neue Konzepte als eigene Ansichten/Modi, nicht als
  zusätzliche Regler im Hauptpanel.
- **Alles teilbar:** Jede neue Ansicht bekommt URL-Parameter, damit Lehrkräfte
  Unterrichtszustände verlinken können.
- **Zweisprachig bleiben** (de/en) und **alle Erklärtexte fachdidaktisch gegenlesen lassen**
  (Lehrstuhl Chemiedidaktik).
