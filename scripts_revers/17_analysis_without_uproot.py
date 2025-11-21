#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ~/physik/scripts/17_analysis_without_uproot.py
Created on Tue Nov  4 16:15:37 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

class ScalarAnalysisNoUproot:
    def __init__(self):
        self.predictions = {
            'mass': 1000.0, 'width': 25.0,
            'coupling_e': 0.001, 'coupling_mu': 0.001, 'coupling_tau': 0.0005,
            'BR_ee': 0.4, 'BR_mumu': 0.4, 'BR_tautau': 0.2
        }

    def simulate_lhc_data(self):
        """Simuliert LHC-ähnliche Daten ohne uproot"""
        np.random.seed(42)  # Für reproduzierbare Ergebnisse

        # Untergrund: Exponentiell fallend
        background_events = 1000
        background = np.random.exponential(50, background_events) + 800

        # Signal: Gaußförmig bei 1000 GeV
        signal_events = 50
        signal = np.random.normal(1000, 10, signal_events)

        return background, signal

    def analyze_sensitivity(self):
        """Analysiere die Nachweisempfindlichkeit"""
        background, signal = self.simulate_lhc_data()

        # Histogramme erstellen
        bins = np.linspace(800, 1200, 80)
        bkg_hist, _ = np.histogram(background, bins=bins)
        sig_hist, _ = np.histogram(signal, bins=bins)

        # Signifikanz berechnen
        signal_bin = np.argmin(np.abs(bins - 1000))
        S = sig_hist[signal_bin] if signal_bin < len(sig_hist) else 0
        B = bkg_hist[signal_bin] if signal_bin < len(bkg_hist) else 1

        significance = S / np.sqrt(B) if B > 0 else 0

        return bins, bkg_hist, sig_hist, significance

    def plot_complete_analysis(self):
        """Erstelle vollständige Analyse-Plots"""
        bins, bkg_hist, sig_hist, current_significance = self.analyze_sensitivity()

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

        # Plot 1: LHC-Signatur
        ax1.step(bins[:-1], bkg_hist, where='post', color='gray', 
                label='Untergrund', linewidth=1.5)
        ax1.step(bins[:-1], bkg_hist + sig_hist, where='post', color='red',
                label='Signal + Untergrund', linewidth=1.5)
        ax1.axvline(1000, color='blue', linestyle='--', 
                   label='Vorhersage: 1000 GeV', linewidth=2)
        ax1.set_xlabel('Invariante Masse [GeV]')
        ax1.set_ylabel('Ereignisse / 5 GeV')
        ax1.set_title('Simulierte LHC-Daten')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Zerfallskanäle
        channels = ['e⁺e⁻', 'μ⁺μ⁻', 'τ⁺τ⁻']
        branching = [0.4, 0.4, 0.2]
        colors = ['red', 'blue', 'green']
        ax2.bar(channels, branching, color=colors, alpha=0.7)
        ax2.set_ylabel('Zerfallsverhältnis')
        ax2.set_title('Zerfallskanäle')
        ax2.grid(True, alpha=0.3)

        # Plot 3: Kopplungsstärken
        couplings = ['e', 'μ', 'τ']
        values = [0.001, 0.001, 0.0005]
        ax3.bar(couplings, values, color=colors, alpha=0.7)
        ax3.set_ylabel('Kopplungsstärke')
        ax3.set_title('Kopplungen an Leptonen')
        ax3.grid(True, alpha=0.3)

        # Plot 4: Signifikanz (KORRIGIERT)
        luminosities = [50, 100, 150, 200, 300]  # fb⁻¹
        # KORREKTUR: current_significance statt sig verwenden
        significances = [current_significance * np.sqrt(lum/140) for lum in luminosities]
        ax4.plot(luminosities, significances, 'o-', linewidth=2, markersize=8)
        ax4.axhline(5, color='red', linestyle='--', label='5σ Entdeckung')
        ax4.set_xlabel('Integrierte Luminosität [fb⁻¹]')
        ax4.set_ylabel('Signifikanz [σ]')
        ax4.set_title('Entdeckungspotential')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('../results/comprehensive_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

        print(f"🔍 Analyse abgeschlossen!")
        print(f"📈 Aktuelle Signifikanz: {current_significance:.1f}σ")
        needed_lumi = 140 * (5/current_significance)**2 if current_significance > 0 else float('inf')
        print(f"💡 Benötigt für 5σ-Entdeckung: {needed_lumi:.0f} fb⁻¹")

# Ausführung
if __name__ == "__main__":
    print("🚀 Starte umfassende Analyse OHNE uproot")
    analysis = ScalarAnalysisNoUproot()
    analysis.plot_complete_analysis()