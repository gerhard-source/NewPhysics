#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/physik/scripts/particle_properties.py
import numpy as np

class ScalarParticleProperties:
    def __init__(self):
        self.properties = {
            'mass': 1000.0,           # GeV
            'width': 25.0,            # GeV
            'spin': 0,
            'parity': '+1',
            'charge': 0,
            'color_charge': 'neutral',
            'is_own_antiparticle': True,  # Wahrscheinlich!
        }
        
        # Kopplungsmatrix an Leptonen
        self.couplings = {
            'electron': 0.00024,
            'muon': 0.00024, 
            'tau': 0.00018,
            'neutrinos': 0.0001,      # Geschätzt
        }
    
    def calculate_quantum_numbers(self):
        """Bestimmt Quantenzahlen basierend auf Kopplungen"""
        # Da es an Leptonen koppelt, aber keine Leptonenzahl trägt
        # → Möglicherweise ein "Lepton-Partner" oder "Scalar Mediator"
        
        return {
            'L_e': 0,      # Elektron-Leptonenzahl
            'L_mu': 0,     # Myon-Leptonenzahl  
            'L_tau': 0,    # Tau-Leptonenzahl
            'B': 0,        # Baryonenzahl
        }
    
    def possible_symmetries(self):
        """Welche Symmetrien könnte es haben?"""
        symmetries = [
            "CP-even (skalar)",      # Wahrscheinlichste Option
            "CP-odd (pseudoskalar)", # Alternative
            "Complex scalar field"   # Dann separates Antiteilchen
        ]
        return symmetries

# Analyse
scalar = ScalarParticleProperties()
quantum_numbers = scalar.calculate_quantum_numbers()
symmetries = scalar.possible_symmetries()

print("🔬 Detaillierte Eigenschaften deines Teilchens:")
for key, value in scalar.properties.items():
    print(f"   {key}: {value}")

print("\n📊 Quantenzahlen:")
for key, value in quantum_numbers.items():
    print(f"   {key}: {value}")

print("\n⚛️ Mögliche Symmetrien:")
for sym in symmetries:
    print(f"   • {sym}")