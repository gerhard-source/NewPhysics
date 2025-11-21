#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ~/physik/scripts/22_cp_properties.py

Created on Tue Nov  4 17:38:07 2025

@author: gh
"""

import numpy as np

class CPAnalysis:
    def __init__(self):
        self.mass = 1000.0
        self.width = 25.0

    def cp_even_signatures(self):
        """Charakteristika für CP-even (skalar)"""
        return {
            'angular_distribution': "1 + cos²θ",  # Typisch für Skalar
            'spin_correlations': "Charakteristisch für Spin-0",
            'production_mechanism': "Gluon-Fusion dominant",
            'decay_angles': "Sphärisch symmetrisch"
        }

    def cp_odd_signatures(self):
        """Charakteristika für CP-odd (pseudoskalar)"""  
        return {
            'angular_distribution': "sin²θ",  # Typisch für Pseudoskalar
            'spin_correlations': "Andere Spin-Korrelationen",
            'production_mechanism': "Gluon-Fusion mit γ5 Kopplung",
            'decay_angles': "Azimutale Asymmetrien"
        }

    def experimental_discrimination(self):
        """Wie Experimente CP-Eigenschaften unterscheiden"""
        discriminators = [
            "Winkelverteilung der Zerfallsleptonen",
            "Spin-Dichtematrix-Analyse", 
            "Produktions-Winkelverteilung",
            "Interferenz mit bekannten Prozessen"
        ]
        return discriminators

# Analyse
cp_study = CPAnalysis()
cp_even = cp_study.cp_even_signatures()
cp_odd = cp_study.cp_odd_signatures()
discriminators = cp_study.experimental_discrimination()

print("🔍 CP-Eigenschaften Analyse:")
print("\n📈 CP-even (skalar) Signaturen:")
for key, value in cp_even.items():
    print(f"   {key}: {value}")

print("\n📉 CP-odd (pseudoskalar) Signaturen:")  
for key, value in cp_odd.items():
    print(f"   {key}: {value}")

print("\n🎯 Experimentelle Unterscheidung:")
for method in discriminators:
    print(f"   • {method}")
