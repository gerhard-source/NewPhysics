#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**6. Starter-Script für die Teilchenjagd:
    
# /home/gh/Schreibtisch/physik/py/scripts/14_scalar_hunt.py

Created on Tue Nov  4 12:57:52 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt
import os

class ReverseReconstructionAnalysis:
    def __init__(self):
        self.mass_prediction = 1000  # GeV - ANPASSEN an deine 5 Parameter!
        self.coupling_strength = 0.1  # ANPASSEN

    def simulate_signal(self):
        """Simuliert das erwartete Signal basierend auf deiner Rückwärtssimulation"""
        # Hier kommen DEINE spezifischen Vorhersagen aus den 5 Parametern
        energy_range = np.linspace(800, 1200, 200)

        # Vorläufige Simulation - mit DEINEN echten Werten ersetzen
        signal = (self.coupling_strength * 
                 np.exp(-0.5*((energy_range - self.mass_prediction)/30)**2))

        return energy_range, signal

    def plot_predictions(self):
        """Visualisiert die Vorhersagen deines Modells"""
        energies, signal = self.simulate_signal()

        plt.figure(figsize=(12, 6))
        plt.plot(energies, signal, 'r-', linewidth=3, 
                label=f'Skalares Teilchen: {self.mass_prediction} GeV')
        plt.xlabel('Invariante Masse [GeV]', fontsize=12)
        plt.ylabel('Erwartetes Signal', fontsize=12)
        plt.title('Vorhersage: Kraftvermittlungsteilchen aus Reverse Reconstruction', fontsize=14)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('./results/scalar_prediction.png', dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    analysis = ReverseReconstructionAnalysis()
    print(f"🔍 Starte Analyse für skalares Teilchen bei {analysis.mass_prediction} GeV")
    analysis.plot_predictions()
