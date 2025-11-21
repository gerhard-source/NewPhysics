#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ~/physik/scripts/23_graviton_analysis.py

Created on Tue Nov  4 17:42:58 2025

@author: gh
"""


class GravitonComparison:
    def __init__(self):
        self.your_particle = {
            'spin': 0,
            'mass': 1000.0,
            'couplings': 'Yukawa (lepton-flavor-universal)',
            'width': 25.0
        }

        self.standard_graviton = {
            'spin': 2,  # Wichtigster Unterschied!
            'mass': 'variabel',
            'couplings': 'universal (an Energie-Impuls-Tensor)',
            'width': 'typisch sehr schmal'
        }

        self.dark_graviton_variants = {
            'massive_graviton': 'Spin-2, aber mit Masse',
            'scalar_graviton': 'Spin-0 Dilaton/Radion',
            'dark_photon_analog': 'Spin-1, aber deins ist Spin-0'
        }

    def compatibility_analysis(self):
        """Analysiert Kompatibilität mit Graviton-Hypothesen"""
        issues = []
        consistencies = []

        # Widersprüche
        if self.your_particle['spin'] != 2:
            issues.append("❌ Spin 0 vs 2: Kein Standard-Graviton")

        if self.your_particle['couplings'] != 'universal':
            issues.append("❌ Nicht-universelle Kopplungen")

        # Konsistenzen
        if self.your_particle['mass'] > 0:
            consistencies.append("✅ Massive: Wie massive Graviton-Varianten")

        if self.your_particle['width'] < 100:  # GeV
            consistencies.append("✅ Endliche Breite: Realistisch")

        return issues, consistencies

# Analyse
comparison = GravitonComparison()
issues, consistencies = comparison.compatibility_analysis()

print("🔍 Graviton-Vergleich:")
print("\n📊 Dein Teilchen vs Standard-Graviton:")
for key in comparison.your_particle:
    print(f"   {key}: {comparison.your_particle[key]} vs {comparison.standard_graviton[key]}")

print("\n⚠️ Widersprüche:")
for issue in issues:
    print(f"   {issue}")

print("\n✅ Konsistenzen:")
for consistency in consistencies:
    print(f"   {consistency}")
