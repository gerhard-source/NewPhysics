#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/physik/scripts/lhc_search.py
import numpy as np
import matplotlib.pyplot as plt
import uproot
from scipy import stats

class LHCScalarSearch:
    def __init__(self):
        # DEINE VORHERSAGEN - direkt von dir übernommen
        self.predictions = {
            'mass': 1000.0,
            'width': 25.0,
            'coupling_e': 0.001,
            'coupling_mu': 0.001, 
            'coupling_tau': 0.0005,
            'branching_ratio_ee': 0.4,
            'branching_ratio_mumu': 0.4,
            'branching_ratio_tautau': 0.2
        }
        
    def expected_significance(self, luminosity=140):  # fb^-1
        """Berechnet die erwartete Signifikanz für LHC-Daten"""
        # Vereinfachte Signifikanzabschätzung
        cross_section = 0.1  # fb - typisch für solche Prozesse
        signal_events = cross_section * luminosity * 0.4  # BR berücksichtigt
        
        background = 50  # Geschätzte Untergrundereignisse im Signalbereich
        significance = signal_events / np.sqrt(background)
        
        return significance
    
    def plot_expected_discovery(self):
        """Zeigt wo dein Signal im LHC-Datensatz erscheinen sollte"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Erwartetes Signalspektrum
        mass_range = np.linspace(800, 1200, 200)
        signal = np.exp(-0.5*((mass_range - self.predictions['mass']) / 
                            (self.predictions['width']/2.355))**2)
        
        background = 1000 * np.exp(-(mass_range-800)/200)
        
        ax1.plot(mass_range, background, 'gray', label='Untergrund', linewidth=2)
        ax1.plot(mass_range, background + signal*50, 'red', 
                label='Signal + Untergrund', linewidth=2)
        ax1.axvline(self.predictions['mass'], color='blue', linestyle='--', 
                   label=f'Vorhersage: {self.predictions["mass"]} GeV')
        ax1.set_xlabel('Invariante Masse [GeV]')
        ax1.set_ylabel('Ereignisse')
        ax1.set_title('Erwartetes Signal im LHC')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Zerfallskanäle
        channels = ['ee', 'μμ', 'ττ']
        branching_ratios = [0.4, 0.4, 0.2]
        
        ax2.bar(channels, branching_ratios, color=['red', 'blue', 'green'])
        ax2.set_ylabel('Zerfallsverhältnis')
        ax2.set_title('Zerfallskanäle des skalaren Teilchens')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../results/lhc_discovery_potential.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return self.expected_significance()

# Analyse durchführen
if __name__ == "__main__":
    print("🔍 Starte LHC-Suche mit deinen Vorhersagen")
    search = LHCScalarSearch()
    significance = search.plot_expected_discovery()
    
    print(f"\n📈 Vorhersagen deines Modells:")
    for key, value in search.predictions.items():
        print(f"   {key}: {value}")
    
    print(f"\n💡 Entdeckungspotential:")
    print(f"   Erwartete Signifikanz: {significance:.1f}σ")
    if significance > 5:
        print("   ✅ Potentiell entdeckbar mit aktuellen LHC-Daten!")
    else:
        print("   🔍 Benötigt mehr Statistik (HL-LHC)")
