#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
halo_simulation.py

Created on Sat Oct 18 15:03:39 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Verzeichnis für Ergebnisse erstellen
results_dir = '../results'
os.makedirs(results_dir, exist_ok=True)

class ScalarDarkMatterHalo:
    def __init__(self, particle_mass=1000.0, coupling_strength=0.0891):
        self.mass = particle_mass  # GeV - DEIN Teilchen!
        self.coupling = coupling_strength
        self.gravitational_constant = 4.3e-6  # kpc (km/s)^2 / M_sun
        
    def nfw_profile(self, r, scale_radius=20.0, scale_density=0.3):
        """Navarro-Frenk-White Dunkle-Materie-Profil"""
        return scale_density / ((r/scale_radius) * (1 + r/scale_radius)**2)
    
    def scalar_field_evolution(self, r, density):
        """Evolution des skalaren Feldes im Halo"""
        # Vereinfachte skalare Feldgleichung
        compton_wavelength = 1.97e-14 / self.mass  # in kpc
        field_amplitude = self.coupling * density * compton_wavelength**2
        return field_amplitude
    
    def simulate_milky_way_halo(self):
        """Simuliert Milchstraßen-Halo mit deinem Teilchen"""
        r_values = np.logspace(-1, 2, 100)  # 0.1 - 100 kpc
        dm_density = np.array([self.nfw_profile(r) for r in r_values])
        scalar_field = np.array([self.scalar_field_evolution(r, dens) 
                               for r, dens in zip(r_values, dm_density)])
        
        return r_values, dm_density, scalar_field
    
    def calculate_halo_energies(self, density_profile, r_values):
        """Berechnet potentielle und kinetische Energie des Halos"""
        # Massenverteilung
        mass_profile = 4 * np.pi * r_values**2 * density_profile
        
        # Potentielle Energie (vereinfacht)
        G = self.gravitational_constant
        total_mass = np.trapz(mass_profile, r_values)
        potential_energy = -G * total_mass**2 / (2 * np.max(r_values))
        
        # Kinetische Energie aus Virialtheorem
        kinetic_energy = -0.5 * potential_energy  # Virialsatz
        
        return potential_energy, kinetic_energy, total_mass
    
    def plot_halo_comparison(self):
        """Vergleicht Standard-DM-Halo mit Skalar-Feld-Modifikation"""
        r, dm_density, scalar_field = self.simulate_milky_way_halo()
        
        # Energieberechnung
        pot_energy, kin_energy, total_mass = self.calculate_halo_energies(dm_density, r)
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
        
        # Plot 1: Dichteprofil
        ax1.loglog(r, dm_density, 'b-', linewidth=2, label='NFW DM Halo')
        ax1.loglog(r, dm_density * (1 + scalar_field), 'r--', linewidth=2, 
                  label='Mit Skalar-Feld Modifikation')
        ax1.set_xlabel('Radius [kpc]')
        ax1.set_ylabel('Dichte [M_sun/kpc³]')
        ax1.set_title('Dunkle-Materie-Dichteprofil der Milchstraße')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Skalar-Feld-Amplitude
        ax2.semilogx(r, scalar_field, 'g-', linewidth=2)
        ax2.set_xlabel('Radius [kpc]')
        ax2.set_ylabel('Skalar-Feld Amplitude')
        ax2.set_title('Stärke des Skalar-Feldes im Halo')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Energie-Informationen
        ax3.axis('off')
        energy_text = (
            f"Energieanalyse des Milchstraßen-Halos:\n\n"
            f"Gesamtmasse: {total_mass:.2e} M☉\n\n"
            f"Potentielle Energie:\n{pot_energy:.2e} M☉·(km/s)²\n"
            f"≈ {pot_energy * 1.99e30 * 1e6:.2e} Joule\n\n"
            f"Kinetische Energie:\n{kin_energy:.2e} M☉·(km/s)²\n"
            f"≈ {kin_energy * 1.99e30 * 1e6:.2e} Joule\n\n"
            f"Teilchen-Masse: {self.mass} GeV\n"
            f"Kopplungsstärke: {self.coupling}"
        )
        ax3.text(0.1, 0.9, energy_text, transform=ax3.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        # Korrigierter Save-Pfad
        save_path = os.path.join(results_dir, 'halo_simulation.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        return pot_energy, kin_energy, total_mass

# Simulation starten
print("🚀 Starte Halo-Simulation mit deinem 1 TeV Skalar-Teilchen...")
halo_sim = ScalarDarkMatterHalo()
pot_energy, kin_energy, total_mass = halo_sim.plot_halo_comparison()

print(f"\n✅ Simulation abgeschlossen!")
print(f"📁 Ergebnis gespeichert in: {os.path.abspath(results_dir)}/halo_simulation.png")
print(f"\n📊 ERGEBNISSE:")
print(f"   Gesamtmasse des Halos: {total_mass:.2e} M☉")
print(f"   Potentielle Energie: {pot_energy:.2e} M☉·(km/s)²")
print(f"   Kinetische Energie: {kin_energy:.2e} M☉·(km/s)²")
print(f"   Virial-Verhältnis: {2*kin_energy/(-pot_energy):.3f} (sollte ≈1.0 sein)")