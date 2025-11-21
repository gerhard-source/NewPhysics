#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 36_create_reverse_simulation_plot.py

Created on Tue Nov  4 19:09:29 2025

@author: gh
"""

import matplotlib.pyplot as plt

def create_reverse_simulation_plot():
    """Visualisierung der Rückwärts-Simulation (wie im vorigen Paper)"""
    steps = [0, 25, 50, 75, 100]
    homogeneity = [0.3, 0.5, 0.7, 0.9, 1.0]
    density_contrast = [1.0, 0.7, 0.4, 0.2, 0.05]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Homogenitätsplot
    ax1.plot(steps, homogeneity, 'o-', linewidth=3, markersize=8, color='#4ECDC4', label='Homogenität')
    ax1.fill_between(steps, homogeneity, alpha=0.3, color='#4ECDC4')
    ax1.set_xlabel('Rückwärts-Schritte', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Homogenität', fontsize=12, fontweight='bold')
    ax1.set_title('Homogenitäts-Entwicklung\n(Rückwärts-Simulation)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Dichtekontrast-Plot
    ax2.plot(steps, density_contrast, 's-', linewidth=3, markersize=8, color='#FF6B6B', label='Dichtekontrast')
    ax2.fill_between(steps, density_contrast, alpha=0.3, color='#FF6B6B')
    ax2.set_xlabel('Rückwärts-Schritte', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Dichtekontrast', fontsize=12, fontweight='bold')
    ax2.set_title('Struktur-Auflösung\n(Rückwärts-Simulation)', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('../paper/figures/reverse_simulation.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Reverse Simulation Plot gespeichert")

create_reverse_simulation_plot()
