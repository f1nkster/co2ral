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

- [ ] **Bjerrum-Diagramm (M)** — das klassische Speziierungsdiagramm (Anteile vs. pH) mit
      Markierung des aktuellen Zustands; Kurvenlage abhängig von T und S → zeigt, dass
      Gleichgewichtskonstanten keine Naturkonstanten des Diagramms sind.
- [ ] **Le-Chatelier-Experimente (M)** — geführte Störungs-Buttons mit Erklärtext:
      „+CO₂ (Verbrennung)", „Erwärmung +5 °C", „Kalk zugeben (Alkalinität ↑)".
      Jeweils Vorher/Nachher-Ansicht und ein Satz Deutung.
- [ ] **Puffer erleben (S)** — Vergleichs-Preset „Meerwasser vs. kalkarmes Süßwasser":
      gleicher CO₂-Eintrag, drastisch anderer pH-Effekt → Alkalinität als Puffer begreifen.

## Phase 3 — Schultauglichkeit

- [ ] **Schulmodus (M)** — eigener Einstieg (z. B. `?mode=schule`): reduzierte Oberfläche
      (nur pCO₂- und Temperatur-Regler, Rest sinnvoll fixiert), vereinfachte Sprache in den
      Erklärtexten, größere Bedienelemente. Kein „Feature-Abbau", sondern didaktische Reduktion.
- [ ] **Alltags-Szenarien (S)** — Presets mit Schulbezug: „Sprudelflasche öffnen",
      „Aquarium im Sommer", „Ozean 1850 / heute / 2100", „Muschelschale in saurem Wasser".
- [ ] **Materialseite für Lehrkräfte (M)** — eigene Seite mit fertigen Unterrichts-Links
      (Share-URLs je Szenario), Aufgabenvorschlägen und Lehrplanbezug; später Arbeitsblätter
      als PDF.
- [ ] **Aufgaben-/Lernpfadmodus (L)** — geführte Erkundungen in der App
      („Stelle pCO₂ auf 280 μatm. Beobachte Ω. Was bedeutet das für Korallen?") mit
      Schritt-Karten. Größtes Einzel-Feature, lohnt erst nach Phase 1+2.

## Phase 4 — Kür & Technik

- [ ] **Teilchen-Animation „dynamisches Gleichgewicht" (L)** — qualitative Animation
      (Hin- und Rückreaktion laufen weiter, Konzentrationen bleiben konstant) gegen die
      Fehlvorstellung „im Gleichgewicht passiert nichts".
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
