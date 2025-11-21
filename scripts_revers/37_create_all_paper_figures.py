#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# 37_create_all_paper_figures.py

Created on Tue Nov  4 19:14:45 2025

@author: gh
"""


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
    print("📁 Gespeichert in: ~/physik/paper/figures/")
    print("🎨 Einfach in LibreOffice Writer einfügen")

# Ausführen
create_all_paper_figures()
