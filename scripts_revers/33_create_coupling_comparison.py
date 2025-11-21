#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 33_create_coupling_comparison.py           fehlerhaft
Created on Tue Nov  4 18:52:21 2025

@author: gh
"""
import matplotlib.pyplot as plt

def create_coupling_comparison():
    """Vergleicht alle Kopplungsstärken"""
    particles = ['e', 'μ', 'τ', 'c', 'b', 't', 'g', 'γ']
    couplings = [0.00024, 0.00024, 0.00018, 0.00066, 0.00217, 0.0891, 0.0134, 0.00057]
    colors = ['#FF9999', '#FF9999', '#FF9999', '#66B2FF', '#66B2FF', '#66B2FF', '#FFD700', '#90EE90']

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(particles, couplings, color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    ax.set_yscale('log')
    ax.set_ylabel('Kopplungsstärke (logarithmisch)', fontsize=14, fontweight='bold')
    ax.set_title('Vergleich der Kopplungsstärken an Standardmodell-Teilchen', fontsize=16, fontweight='bold')

    # Werte anzeigen
    for bar, coupling in zip(bars, couplings):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.2,
                f'{coupling:.1e}', ha='center', va='bottom', fontsize=10, rotation=45)

    # Legende
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF9999', label='Leptonen'),
        Patch(facecolor='#66B2FF', label='Quarks'),
        Patch(facecolor='#FFD700', label='Gluonen'),
        Patch(facecolor='#90EE90', label='Photonen')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('../paper/figures/coupling_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Coupling Comparison gespeichert")

create_coupling_comparison()
