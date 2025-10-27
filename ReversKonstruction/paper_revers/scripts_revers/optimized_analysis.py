#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/physik/scripts/optimized_analysis.py
import numpy as np
import matplotlib.pyplot as plt

class OptimizedAnalysis:
    def __init__(self):
        self.optimized_params = {
            'mass': 1000.0, 'width': 25.0,
            'coupling_e': 0.00024, 'coupling_mu': 0.00024, 'coupling_tau': 0.00018,
            'BR_ee': 0.36, 'BR_mumu': 0.36, 'BR_tautau': 0.28
        }
    
    def calculate_expected_significance(self):
        """Berechnet Signifikanz mit optimierten Parametern"""
        # Signifikanz skaliert mit Kopplung^2
        coupling_reduction = (0.00024 / 0.001)  # 0.24
        original_significance = 11.0  # Dein vorheriges Ergebnis
        new_significance = original_significance * coupling_reduction**2
        
        return new_significance
    
    def plot_comparison(self):
        """Vergleicht ursprüngliche und optimierte Vorhersagen"""
        original_sig = 11.0
        optimized_sig = self.calculate_expected_significance()
        
        # Luminosität für 5σ Entdeckung
        lumi_original = 140 * (5/original_sig)**2
        lumi_optimized = 140 * (5/optimized_sig)**2 if optimized_sig > 0 else float('inf')
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Signifikanz-Vergleich
        labels = ['Ursprünglich', 'Optimiert']
        significances = [original_sig, optimized_sig]
        colors = ['red', 'blue']
        
        bars = ax1.bar(labels, significances, color=colors, alpha=0.7)
        ax1.axhline(5, color='green', linestyle='--', label='5σ Entdeckung')
        ax1.set_ylabel('Signifikanz [σ]')
        ax1.set_title('Vorhersage-Vergleich')
        ax1.legend()
        
        # Werte in Balken schreiben
        for bar, sig in zip(bars, significances):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{sig:.1f}σ', ha='center', va='bottom')
        
        # Benötigte Luminosität
        luminosities = [lumi_original, lumi_optimized]
        bars2 = ax2.bar(labels, luminosities, color=colors, alpha=0.7)
        ax2.set_ylabel('Benötigte Luminosität [fb⁻¹]')
        ax2.set_title('Luminosität für 5σ-Entdeckung')
        
        for bar, lum in zip(bars2, luminosities):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    f'{lum:.0f} fb⁻¹', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('../results/optimized_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"📊 Vergleich der Vorhersagen:")
        print(f"   Ursprünglich: {original_sig:.1f}σ (benötigt {lumi_original:.0f} fb⁻¹)")
        print(f"   Optimiert:    {optimized_sig:.1f}σ (benötigt {lumi_optimized:.0f} fb⁻¹)")

# Ausführung
analysis = OptimizedAnalysis()
analysis.plot_comparison()