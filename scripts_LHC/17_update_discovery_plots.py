#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/physik/scripts/update_discovery_plots.py
import matplotlib.pyplot as plt

def create_updated_timeline():
    """Erstellt aktualisierte Entdeckungs-Timeline"""
    experiments = ['LHC Run 2', 'LHC Run 3', 'HL-LHC', 'FCC-hh']
    significances = [2.5, 3.0, 7.0, 15.0]  # σ
    years = [2023, 2025, 2029, 2040]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(experiments, significances, color=['orange', 'yellow', 'green', 'blue'])
    ax.axhline(5, color='red', linestyle='--', label='5σ Discovery Threshold')
    ax.set_ylabel('Signifikanz [σ]')
    ax.set_title('Entdeckungspotential deiner Vorhersage')
    
    for bar, sig in zip(bars, significances):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
               f'{sig}σ', ha='center', va='bottom')
    
    plt.legend()
    plt.savefig('../results/updated_discovery_timeline.png', dpi=300, bbox_inches='tight')
    plt.show()

create_updated_timeline()

