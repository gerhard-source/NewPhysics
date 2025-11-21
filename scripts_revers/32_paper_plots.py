#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ~/physik/scripts/32_paper_plots.py  fehlerhaft

Created on Tue Nov  4 18:47:55 2025

@author: gh
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 12, 'figure.figsize': (10, 6)})

def create_discovery_timeline():
    """Erstellt die Entdeckungszeitachse für das Paper"""
    experiments = ['LHC Run 2\n(aktuell)', 'LHC Run 3\n(2025+)', 'HL-LHC\n(2029+)', 'FCC-hh\n(2040+)']
    significances = [2.5, 3.0, 7.0, 15.0]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(experiments, significances, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    # 5σ Entdeckungslinie
    ax.axhline(y=5, color='red', linestyle='--', linewidth=3, label='5σ Entdeckungsschwelle', alpha=0.8)

    # Werte in Balken schreiben
    for bar, sig in zip(bars, significances):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{sig}σ', ha='center', va='bottom', fontsize=14, fontweight='bold')

    ax.set_ylabel('Statistische Signifikanz [σ]', fontsize=14, fontweight='bold')
    ax.set_title('Entdeckungspotential der 1 TeV Skalar-Resonanz', fontsize=16, fontweight='bold')
    ax.legend(loc='upper left', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 18)

    plt.tight_layout()
    plt.savefig('../paper/figures/discovery_timeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Discovery Timeline gespeichert")

create_discovery_timeline()
