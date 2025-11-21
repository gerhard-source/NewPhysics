#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ~/physik/scripts/26_quark_gluon_couplings.py

Created on Tue Nov  4 18:05:07 2025

@author: gh
"""

import numpy as np

class QuarkGluonCouplings:
    def __init__(self):
        # DEINE 5 primordiale Parameter
        self.primordial_params = {
            'E': 0.0063,      # Primordial Energy
            'g': 0.3028,      # Primordial Coupling  
            'S': -0.2003,     # Primordial Symmetry
            'Y': 0.0814,      # Yukawa Parameter
            'Φ': 1.0952       # Flavor Parameter
        }

        # Bekannte Lepton-Kopplungen (aus deiner Analyse)
        self.known_lepton_couplings = {
            'electron': 0.00024,
            'muon': 0.00024,
            'tau': 0.00018
        }

    def calculate_dilaton_couplings(self):
        """Berechnet Dilaton-artige Kopplungen basierend auf Standardmodell-Beta-Funktionen"""

        # Dilaton koppelt an Spur des Energie-Impuls-Tensors
        # Kopplungsstärken skaliert mit Beta-Funktionen und Anomaliedimensionen

        # Für Fermionen: ∝ γ_m (anomale Dimension) ≈ masse_proportional
        # Für Eichbosonen: ∝ β_g/g (Beta-Funktion)

        # Basierend auf deinen Parametern:
        base_coupling = self.primordial_params['Y']  # Yukawa-basiert

        # Quark-Kopplungen (masse-proportional wie bei Dilaton)
        quark_masses_mev = {
            'up': 2.2, 'down': 4.7, 'charm': 1270, 
            'strange': 93, 'top': 172000, 'bottom': 4180
        }

        # Normierung auf Top-Quark (stärkste Kopplung)
        max_quark_mass = max(quark_masses_mev.values())

        quark_couplings = {}
        for quark, mass in quark_masses_mev.items():
            # Masse-proportionale Kopplung + Flavor-Faktor aus Φ
            coupling = (base_coupling * (mass / max_quark_mass) * 
                       self.primordial_params['Φ'])
            quark_couplings[quark] = coupling

        # Gluon-Kopplung (stark wegen QCD Beta-Funktion)
        # β_QCD ≈ 7 - typisch groß
        qcd_beta_function = 7.0
        gluon_coupling = (self.primordial_params['g'] * qcd_beta_function * 
                         self.primordial_params['E'])

        # Photon-Kopplung (QED Beta-Funktion ist klein)
        qed_beta_function = -0.3  # Negativ für U(1)
        photon_coupling = (self.primordial_params['g'] * abs(qed_beta_function) * 
                          self.primordial_params['E'])

        return {
            'quarks': quark_couplings,
            'gluons': gluon_coupling,
            'photons': photon_coupling
        }

    def calculate_branching_ratios(self, couplings):
        """Berechnet Zerfallsverhältnisse basierend auf Kopplungen"""

        # Zerfallsbreiten skaliert mit coupling^2 * phase_space

        # Für skalares Teilchen bei 1000 GeV
        mass = 1000.0  # GeV

        # Phase space Faktoren (vereinfacht)
        phase_space = {
            'leptons': 1.0,      # e⁺e⁻, μ⁺μ⁻, τ⁺τ⁻
            'quarks': 3.0,       # Farbfaktor
            'gluons': 8.0,       # 8 Gluonen
            'photons': 1.0
        }

        # Berechne partielle Zerfallsbreiten
        partial_widths = {}

        # Lepton-Zerfälle (bekannt aus deiner Analyse)
        lepton_width = sum([c**2 for c in self.known_lepton_couplings.values()]) * phase_space['leptons']
        partial_widths['leptons'] = lepton_width

        # Quark-Zerfälle
        quark_width = sum([c**2 for c in couplings['quarks'].values()]) * phase_space['quarks']
        partial_widths['quarks'] = quark_width

        # Gluon-Zerfall
        gluon_width = couplings['gluons']**2 * phase_space['gluons']
        partial_widths['gluons'] = gluon_width

        # Photon-Zerfall  
        photon_width = couplings['photons']**2 * phase_space['photons']
        partial_widths['photons'] = photon_width

        # Total width
        total_width = sum(partial_widths.values())

        # Branching ratios
        branching_ratios = {channel: width/total_width for channel, width in partial_widths.items()}

        return branching_ratios, partial_widths

# Berechnung durchführen
coupling_calculator = QuarkGluonCouplings()
calculated_couplings = coupling_calculator.calculate_dilaton_couplings()
branching_ratios, partial_widths = coupling_calculator.calculate_branching_ratios(calculated_couplings)

print("🔬 BERECHNETE QUARK/GLUON-KOPPLUNGEN:")
print("\n📊 Quark-Kopplungen:")
for quark, coupling in calculated_couplings['quarks'].items():
    print(f"   {quark:8}: {coupling:.6f}")

print(f"\n📊 Gluon-Kopplung:  {calculated_couplings['gluons']:.6f}")
print(f"📊 Photon-Kopplung: {calculated_couplings['photons']:.6f}")

print("\n🎯 VORHERSAGE FÜR ZERFALLSVERHÄLTNISSE:")
for channel, ratio in branching_ratios.items():
    print(f"   {channel:8}: {ratio*100:.2f}%")

print("\n📈 PARTIELLE ZERFALLSBREITEN:")
for channel, width in partial_widths.items():
    print(f"   {channel:8}: {width:.6f}")
