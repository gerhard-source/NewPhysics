#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/physik/scripts/future_prospects.py
import matplotlib.pyplot as plt
import numpy as np

class FutureProspects:
    def __init__(self):
        self.facilities = {
            'HL-LHC (2029-)': 3000,      # fb⁻¹
            'FCC-hh (2040+)': 30000,     # fb⁻¹  
            'CLIC (2035+)': 5000,        # fb⁻¹
            'Muon Collider (2040+)': 10000  # fb⁻¹
        }
        
        self.required_lumi = 8718  # fb⁻¹ aus deiner Berechnung
    
    def plot_discovery_timeline(self):
        """Zeigt wann dein Teilchen entdeckt werden könnte"""
        facilities = list(self.facilities.keys())
        luminosities = list(self.facilities.values())
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Timeline-Plot
        years = [2029, 2040, 2035, 2040]
        colors = ['orange', 'red', 'blue', 'green']
        
        for i, (facility, lumi, year, color) in enumerate(zip(facilities, luminosities, years, colors)):
            discovery_prob = min(100, (lumi / self.required_lumi) * 100)
            ax1.barh(facility, discovery_prob, color=color, alpha=0.7)
            ax1.text(discovery_prob + 2, i, f'{discovery_prob:.0f}%', va='center')
        
        ax1.axvline(100, color='red', linestyle='--', label='100% Entdeckung')
        ax1.set_xlabel('Entdeckungswahrscheinlichkeit [%]')
        ax1.set_title('Wann dein Teilchen entdeckt werden könnte')
        ax1.grid(True, alpha=0.3)
        
        # Luminositäts-Vergleich
        facilities_extended = ['LHC (aktuell)'] + facilities
        luminosities_extended = [200] + luminosities
        
        ax2.bar(facilities_extended, luminosities_extended, 
               color=['gray'] + colors, alpha=0.7)
        ax2.axhline(self.required_lumi, color='red', linestyle='--', 
                   label=f'Benötigt: {self.required_lumi} fb⁻¹')
        ax2.set_ylabel('Integrierte Luminosität [fb⁻¹]')
        ax2.set_title('Vergleich der Beschleuniger')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../results/future_discovery.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("🔭 Zukünftige Entdeckungsmöglichkeiten:")
        for facility, lumi in self.facilities.items():
            probability = min(100, (lumi / self.required_lumi) * 100)
            print(f"   {facility}: {probability:.0f}% Wahrscheinlichkeit")

# Analyse
prospects = FutureProspects()
prospects.plot_discovery_timeline()
