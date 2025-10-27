# NewPhysics
## Lizenz
MIT License – frei für Forschung.

**Autor**: Dr. rer. nat. Gerhard Heymel (@DenkRebell)  
**Datum**: 22. Oktober 2025  
**Kontakt**: [x.com/DenkRebell](https://x.com/DenkRebell)

## Reverse Reconstruction: Emergent Physics from 5 Primordial Parameters

![GitHub Repo stars](https://img.shields.io/github/stars/DenkRebell/reverse-reconstruction-physics?style=social)

### Abstract (Englisch)
A Reverse Reconstruction method derives the 18 Standard Model constants from 5 primordial parameters (E=0.0063, g=0.3028, σ=-0.2003, Y=0.0814, Φ=1.0952) with 1–3% accuracy. Key prediction: 1 TeV scalar resonance (Γ=25.3 MeV, 85% top decays). Solves fine-tuning via mathematical emergence.

### Zusammenfassung (Deutsch)
Eine Reverse-Rekonstruktions-Methode leitet die 18 SM-Konstanten aus 5 primordialen Parametern ab. Kernvorhersage: Skalare Resonanz bei 1 TeV. Lösung des Feinabstimmungsproblems durch Emergenz.

### Inhalte
- **Code**: `reverse_reconstruction.py` – SymPy-Simulationen für Iteration, Emergenz (SM, Neutrinos, DM/WIMP/FDM, DE, GW-DE-Modulation).
- **Papers**: 
  - Englisch: [paper_en_gw_extended_final.pdf](paper_en_gw_extended_final.pdf)
  - Deutsch: [paper_de_gw_extended_final.pdf](paper_de_gw_extended_final.pdf)
- **Visuals**: Konvergenz-Plots, GW-Dämpfung, kosmologische Anteile (siehe `/figs/`).

### Installation & Ausführung
1. Klonen: `git clone https://github.com/DenkRebell/reverse-reconstruction-physics.git`
2. Abhängigkeiten: `pip install sympy numpy matplotlib`
3. Ausführen: `python reverse_reconstruction.py` – Erzeugt Outputs und Plots.

### Kernvorhersagen
| Parameter | Wert | Testbar bei |
|-----------|------|-------------|
| Higgs-Masse | 125.0 GeV | LHC |
| DM (WIMP) | 1000 GeV | HL-LHC |
| Ω_Λ (DE) | 0.680 | DESI/Euclid |
| GW-Strain h_mod | 9.50e-22 | LISA |

## HaloSimulation

## Emergente-LQG-Simulation

### Abstract 
Diese Arbeit präsentiert eine Simulationsstudie zur reverse Rekon-
struktion von Spin-Netzwerken in der Loop Quantum Gravity (LQG).
Ausgehend von einem komplexen, inhomogenen “heutigen” Zustand
wird durch inverse Operationen (Kanten- und Knoten-Verschmelzungen)
ein primordialer, homogener Zustand rekonstruiert. Die Simulation de-
monstriert die Konvergenz zu hoher Homogenität und kollabierendem
Volumen, was eine Quantensingularität im Planck-Regime andeutet.
Mathematische Grundlagen, Implementierung und Ergebnisse werden
detailliert beschrieben.

### Zusammenfassung
Die Simulation rekonstruiert erfolgreich einen primordialen Zustand, unter-
streicht LQG’s Singularitäts-Auflösung. Die Visualisierung in Abbildung 1
betont die Überführung von Inhomogenität zu Symmetrie. Erweiterungen:
Stochastische Auswahl, volle Intertwiner.

### Ergebnisse
Ausgehend von H = 0.672 (6 Knoten, 12 Kanten) konvergiert die Simulation
in 2 Schritten zu H = 0.876 (4 Knoten, 3 Kanten, Vtotal = 0). Entwicklung:

| Schritt|Knoten| Kanten |  H  | Vtota |
|--------|------|--------------|-------|
|    0   |   6  |   12   |0.672| ∼ 0.8 |
|    1   |   5  |    9   |0.701| ∼ 0.6 |
|    2   |   4  |    3   |0.876| 0.000 |

Tabelle 1: Entwicklung der Metriken.



### Inhalte
- **Code**: `Spin_Netzwerk_Klasse_Demo.py, demo_reverse_simulation.py`
` – SymPy-Simulationen für Iteration, Emergenz.
- **Papers**: 
  - Englisch: [paper String-Loop-Modell-en.pdf](String-Loop-Modell-en.pdf)
  - Deutsch: [paper String-Loop-Modell-de.pdf](String-Loop-Modell-de.pdf)
- **Visuals**: Konvergenz-Plots (siehe `/scritps/figures/`).

### Installation & Ausführung
1. Klonen: `git clone https://github.com/DenkRebell/reverse-reconstruction-physics.git`
2. Abhängigkeiten: `pip install sympy numpy matplotlib`
3. Ausführen: `Spin_Netzwerk_Klasse_Demo.py, demo_reverse_simulation.py` 
   – Erzeugt Outputs und Plots.

### Diskussion und Ausblick

Die Simulation rekonstruiert erfolgreich einen primordialen Zustand, unter-
streicht LQG’s Singularitäts-Auflösung. Die Visualisierung in Abbildung 1
betont die Überführung von Inhomogenität zu Symmetrie. Erweiterungen:
Stochastische Auswahl, volle Intertwiner.
