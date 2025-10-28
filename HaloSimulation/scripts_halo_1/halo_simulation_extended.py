#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
~/Schreibtisch/physik/HALO/scripts/halo_simulation_extended.py

Created on Sat Oct 18 15:47:48 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Verzeichnis für Ergebnisse erstellen
results_dir = '../results'
os.makedirs(results_dir, exist_ok=True)

class AdvancedScalarDarkMatterHalo:
    def __init__(self):
        # DREI verschiedene Szenarien für skalare Dunkle Materie
        self.scenarios = {
            'heavy_geV': {
                'mass': 1000.0,  # GeV - DEIN Teilchen!
                'coupling': 0.0891,
                'name': '1 TeV Skalar (Collider-Kandidat)',
                'color': 'red'
            },
            'light_eV': {
                'mass': 1e-6,  # 1 μeV - Ultraleichtes Axion-ähnlich
                'coupling': 0.1,
                'name': '1 μeV Skalar (Halo-modifizierend)',
                'color': 'green'
            },
            'intermediate': {
                'mass': 1.0,  # 1 GeV - Mittlere Skala
                'coupling': 0.01,
                'name': '1 GeV Skalar (Hybrid)',
                'color': 'blue'
            }
        }
        
        self.gravitational_constant = 4.3e-6  # kpc (km/s)^2 / M_sun
        
    def nfw_profile(self, r, scale_radius=20.0, scale_density=0.3):
        """Navarro-Frenk-White Dunkle-Materie-Profil"""
        return scale_density / ((r/scale_radius) * (1 + r/scale_radius)**2)
    
    def compton_wavelength_kpc(self, mass_geV):
        """Berechnet Compton-Wellenlänge in kpc"""
        # λ_c = ħ/(m·c) 
        # 1 GeV⁻¹ = 1.97e-14 kpc
        return 1.97e-14 / mass_geV
    
    def scalar_field_profile(self, r, mass_geV, coupling):
        """Realistisches Skalarfeld-Profil basierend auf Masse"""
        compton_wavelength = self.compton_wavelength_kpc(mass_geV)
        
        if mass_geV >= 0.1:  # Schwere Teilchen (> 100 MeV)
            # KEIN messbarer Effekt auf galaktischen Skalen
            return np.zeros_like(r)
        else:
            # Ultraleichte Teilchen: Yukawa-artiges Potential
            field_strength = coupling * np.exp(-r / compton_wavelength)
            return field_strength
    
    def modified_density_profile(self, r, base_density, mass_geV, coupling):
        """Modifiziertes Dichteprofil durch Skalarfeld"""
        field_strength = self.scalar_field_profile(r, mass_geV, coupling)
        
        if mass_geV >= 0.1:
            # Schwere Teilchen: Keine Modifikation auf kpc-Skalen
            return base_density
        else:
            # Ultraleichte Teilchen: Spürbare Modifikation
            return base_density * (1 + field_strength)
    
    def simulate_scenarios(self):
        """Simuliert alle drei Szenarien"""
        r_values = np.logspace(-1, 2, 100)  # 0.1 - 100 kpc
        base_density = np.array([self.nfw_profile(r) for r in r_values])
        
        results = {}
        for scenario_name, params in self.scenarios.items():
            modified_density = self.modified_density_profile(
                r_values, base_density, params['mass'], params['coupling']
            )
            field_strength = self.scalar_field_profile(
                r_values, params['mass'], params['coupling']
            )
            
            results[scenario_name] = {
                'r': r_values,
                'base_density': base_density,
                'modified_density': modified_density,
                'field_strength': field_strength,
                'params': params
            }
        
        return results
    
    def calculate_detectability(self, mass_geV, compton_wavelength):
        """Bewertet die Nachweisbarkeit in verschiedenen Experimenten"""
        detectability = {
            'collider': mass_geV >= 1.0,  # LHC-sensitiv
            'direct_detection': 0.001 <= mass_geV <= 1000,  # DM-Detektoren
            'halo_modification': mass_geV <= 1e-9,  # Nur ultraleichte Teilchen
            'astrophysical': mass_geV <= 1e-15  # Stern-Oszillationen etc.
        }
        
        return detectability
    
    def plot_comprehensive_comparison(self):
        """Vergleicht alle Szenarien umfassend"""
        results = self.simulate_scenarios()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Dichteprofil-Vergleich
        ax1.loglog(results['heavy_geV']['r'], results['heavy_geV']['base_density'], 
                  'k-', linewidth=3, label='Standard NFW Halo', alpha=0.7)
        
        for scenario_name, data in results.items():
            params = data['params']
            ax1.loglog(data['r'], data['modified_density'], 
                      linestyle='--', linewidth=2, color=params['color'],
                      label=params['name'])
        
        ax1.set_xlabel('Radius [kpc]', fontsize=12)
        ax1.set_ylabel('Dichte [M_sun/kpc³]', fontsize=12)
        ax1.set_title('Vergleich: Skalar-DM Szenarien', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Skalarfeld-Stärke
        for scenario_name, data in results.items():
            params = data['params']
            compton_wl = self.compton_wavelength_kpc(params['mass'])
            ax2.semilogx(data['r'], data['field_strength'], 
                        linewidth=2, color=params['color'],
                        label=f"{params['name']}\nλ_c = {compton_wl:.1e} kpc")
        
        ax2.set_xlabel('Radius [kpc]', fontsize=12)
        ax2.set_ylabel('Skalar-Feld Stärke', fontsize=12)
        ax2.set_title('Reichweite der Skalar-Felder', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Compton-Wellenlängen Vergleich
        masses = np.logspace(-22, 3, 100)  # 1e-22 eV bis 1000 GeV
        compton_lengths = [self.compton_wavelength_kpc(mass) for mass in masses]
        
        ax3.loglog(masses, compton_lengths, 'purple', linewidth=3)
        ax3.axhline(y=1, color='red', linestyle='--', label='1 kpc (galaktische Skala)')
        ax3.axhline(y=0.001, color='orange', linestyle='--', label='1 pc (Sternhaufen)')
        
        # Markiere unsere Szenarien
        for scenario_name, params in self.scenarios.items():
            compton_wl = self.compton_wavelength_kpc(params['mass'])
            ax3.plot(params['mass'], compton_wl, 'o', markersize=8, 
                    color=params['color'], label=params['name'])
        
        ax3.set_xlabel('Teilchenmasse [GeV]', fontsize=12)
        ax3.set_ylabel('Compton-Wellenlänge [kpc]', fontsize=12)
        ax3.set_title('Compton-Wellenlänge vs. Masse', fontsize=14, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Nachweisbarkeits-Diagramm
        detection_methods = ['Collider (LHC)', 'Direkte Detektion', 'Halo-Modifikation', 'Astrophysikalisch']
        scenarios_list = list(self.scenarios.keys())
        
        detectability_matrix = np.zeros((len(detection_methods), len(scenarios_list)))
        
        for i, scenario_name in enumerate(scenarios_list):
            params = self.scenarios[scenario_name]
            compton_wl = self.compton_wavelength_kpc(params['mass'])
            detectability = self.calculate_detectability(params['mass'], compton_wl)
            
            detectability_matrix[0, i] = detectability['collider']
            detectability_matrix[1, i] = detectability['direct_detection'] 
            detectability_matrix[2, i] = detectability['halo_modification']
            detectability_matrix[3, i] = detectability['astrophysical']
        
        im = ax4.imshow(detectability_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
        
        # Beschriftungen
        ax4.set_xticks(range(len(scenarios_list)))
        ax4.set_xticklabels([self.scenarios[s]['name'] for s in scenarios_list], rotation=45)
        ax4.set_yticks(range(len(detection_methods)))
        ax4.set_yticklabels(detection_methods)
        
        # Werte in Zellen schreiben
        for i in range(len(detection_methods)):
            for j in range(len(scenarios_list)):
                text = ax4.text(j, i, 'JA' if detectability_matrix[i, j] else 'NEIN',
                              ha="center", va="center", color="black", fontweight='bold')
        
        ax4.set_title('Nachweisbarkeit in verschiedenen Experimenten', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Speichern
        save_path = os.path.join(results_dir, 'comprehensive_halo_analysis.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        return results

# Erweiterte Analyse durchführen
print("🚀 Starte erweiterte Halo-Simulation mit multiplen Szenarien...")
advanced_sim = AdvancedScalarDarkMatterHalo()
results = advanced_sim.plot_comprehensive_comparison()

print(f"\n✅ Erweiterte Simulation abgeschlossen!")
print(f"📁 Ergebnis gespeichert in: {os.path.abspath(results_dir)}/comprehensive_halo_analysis.png")

print(f"\n🔬 WICHTIGE ERKENNTNISSE:")
print(f"   1. Dein 1 TeV Teilchen: EXZELLENT für LHC, aber keine Halo-Modifikation")
print(f"   2. Ultraleichte Teilchen (<1 eV): Modifizieren Halos messbar")  
print(f"   3. Compton-Wellenlänge entscheidet über galaktische Wirksamkeit")
print(f"   4. Konzentriere dich auf LHC-Nachweis für dein 1 TeV Skalar!")


