#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 35_create_significance_projection.py

Created on Tue Nov  4 19:04:56 2025

@author: gh
"""

import matplotlib.pyplot as plt

def create_significance_projection():
    """Projektion der Signifikanz über integrierter Luminosität"""
    luminosities = [50, 100, 150, 200, 300, 1000, 3000]  # fb⁻¹
    significances = [0.8, 1.1, 1.4, 1.6, 2.0, 3.7, 6.4]  # σ

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(luminosities, significances, 'o-', linewidth=3, markersize=8, 
            color='#FF6B6B', markerfacecolor='white', markeredgewidth=2)

    ax.axhline(y=5, color='red', linestyle='--', linewidth=2, label='5σ Entdeckung', alpha=0.8)
    ax.axvline(x=140, color='blue', linestyle=':', linewidth=2, label='Aktuelle LHC-Daten', alpha=0.7)
    ax.axvline(x=3000, color='green', linestyle=':', linewidth=2, label='HL-LHC Ziel', alpha=0.7)

    ax.set_xlabel('Integrierte Luminosität [fb⁻¹]', fontsize=14, fontweight='bold')
    ax.set_ylabel('Statistische Signifikanz [σ]', fontsize=14, fontweight='bold')
    ax.set_title('Signifikanz-Projektion über Luminosität', fontsize=16, fontweight='bold')
    ax.legend(loc='lower right', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 3200)
    ax.set_ylim(0, 8)

    # Wichtige Punkte markieren
    ax.annotate('Aktuell: 2-3σ', xy=(140, 2.5), xytext=(200, 3.5),
                arrowprops=dict(arrowstyle='->', color='black'), fontsize=11, fontweight='bold')

    ax.annotate('HL-LHC: >7σ', xy=(3000, 6.4), xytext=(2000, 5.5),
                arrowprops=dict(arrowstyle='->', color='black'), fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('../paper/figures/significance_projection.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Significance Projection gespeichert")

create_significance_projection()
