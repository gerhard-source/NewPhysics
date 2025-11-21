#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ~/physik/scripts/25_dilaton_predictions.py

Created on Tue Nov  4 17:57:39 2025

@author: gh
"""


def calculate_dilaton_couplings(your_5_parameters):
    """Berechnet erwartete Dilaton-Kopplungen aus deinen Parametern"""
    # E, g, S, Y, Φ → Dilaton-Kopplungen
    predicted_couplings = {
        'gluons': your_5_parameters['g'] * 0.1,  # Beispiel
        'photons': your_5_parameters['E'] * 0.01,
        'leptons': your_5_parameters['Y'],  # Deine bekannte Kopplung
        'quarks': your_5_parameters['Y'] * 0.1  # Geschätzt
    }
    return predicted_couplings

# Test mit deinen Werten
your_params = {'E': 0.0063, 'g': 0.3028, 'S': -0.2003, 'Y': 0.0814, 'Φ': 1.0952}
dilaton_couplings = calculate_dilaton_couplings(your_params)

print("🔮 Dilaton-Vorhersagen aus deinen 5 Parametern:")
for particle, coupling in dilaton_couplings.items():
    print(f"   {particle}: {coupling:.6f}")
