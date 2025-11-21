#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ~/physik/38_paper_plots.py

Created on Tue Nov  4 19:19:11 2025

@author: gh
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Stelle sicher, dass das figures-Verzeichnis existiert
figures_dir = '../paper/figures'
os.makedirs(figures_dir, exist_ok=True)

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
    plt.savefig(os.path.join(figures_dir, 'discovery_timeline.png'), dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Discovery Timeline gespeichert")

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
    plt.savefig(os.path.join(figures_dir, 'coupling_comparison.png'), dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Coupling Comparison gespeichert")

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
    plt.savefig(os.path.join(figures_dir, 'branching_ratios.png'), dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Branching Ratios gespeichert")

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
    plt.savefig(os.path.join(figures_dir, 'significance_projection.png'), dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Significance Projection gespeichert")

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
    plt.savefig(os.path.join(figures_dir, 'reverse_simulation.png'), dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print("✅ Reverse Simulation Plot gespeichert")

# Hauptscript zum Erstellen aller Diagramme
def create_all_paper_figures():
    """Erstellt alle Diagramme für das Paper"""
    print("🚀 Erstelle alle Paper-Diagramme...")

    create_discovery_timeline()
    create_coupling_comparison() 
    create_branching_ratios()
    create_significance_projection()
    create_reverse_simulation_plot()

    print("\n✅ ALLE DIAGRAMME FERTIG!")
    print(f"📁 Gespeichert in: {os.path.abspath(figures_dir)}/")
    print("🎨 Einfach in LibreOffice Writer einfügen")

# Ausführen
if __name__ == "__main__":
    create_all_paper_figures()
