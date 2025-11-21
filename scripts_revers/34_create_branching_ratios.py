#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 34_create_branching_ratios.py
Created on Tue Nov  4 18:57:12 2025

@author: gh
"""
import matplotlib.pyplot as plt

def create_branching_ratios():
    """Erstellt Kuchendiagramm der Zerfallsverhältnisse"""
    channels = ['t̄t', 'bb̄', 'cc̄', 'e⁺e⁻', 'μ⁺μ⁻', 'τ⁺τ⁻', 'gg', 'γγ']
    ratios = [85, 8, 4, 1, 1, 0.5, 0.5, 0.1]
    colors = ['#FF6B6B', '#FF8E72', '#FFA07A', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFD700', '#90EE90']

    # Nur Kanäle > 0.5% anzeigen
    significant_channels = []
    significant_ratios = []
    significant_colors = []

    for channel, ratio, color in zip(channels, ratios, colors):
        if ratio >= 0.5:
            significant_channels.append(channel)
            significant_ratios.append(ratio)
            significant_colors.append(color)

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(significant_ratios, labels=significant_channels, colors=significant_colors,
                                      autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})

    # Prozente fett machen
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title('Zerfallsverhältnisse der 1 TeV Skalar-Resonanz', fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('../paper/figures/branching_ratios.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Branching Ratios gespeichert")

create_branching_ratios()
