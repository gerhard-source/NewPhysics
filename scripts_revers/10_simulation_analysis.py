#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 10_simulation_analysis.py
Created on Tue Nov  4 09:56:32 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Zuerst simulieren wir theoretische Vorhersagen
def simulate_scalar_resonance(mass=1000, width=10, coupling_strength=0.1):
    """Simuliert das erwartete Signal eines skalaren Resonanz-Teilchens"""
    energy_bins = np.linspace(800, 1200, 100)  # Bereich um 1 TeV
    signal = coupling_strength * np.exp(-0.5*((energy_bins - mass)/width)**2)
    return energy_bins, signal

# 2. Untergrund modellieren (typische QCD-Hintergrund)
def simulate_background():
    energy_bins = np.linspace(800, 1200, 100)
    background = 1000 * np.exp(-energy_bins/300)  #Exponentiell fallend
    return energy_bins, background

# 3. Kombiniertes Spektrum plotten
def plot_expected_signature():
    energies, signal = simulate_scalar_resonance()
    _, background = simulate_background()

    plt.figure(figsize=(10, 6))
    plt.plot(energies, background, 'b-', label='Erwarteter Untergrund', linewidth=2)
    plt.plot(energies, background + signal, 'r-', label='Untergrund + Signal', linewidth=2)
    plt.xlabel('Invariante Masse [GeV]')
    plt.ylabel('Ereignisse')
    plt.title('Erwartetes Signal bei ~1 TeV')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_expected_signature()
