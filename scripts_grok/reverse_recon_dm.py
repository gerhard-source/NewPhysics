#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

reverse_recon_dm.py

Created on Tue Oct 21 11:30:21 2025

@author: gh
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt  # Für optionale Plots

class ReverseReconstruction:
    """
    Modulare Klasse für die Reverse-Rekonstruktion: Iteration zu Urparametern,
    Emergenz von SM-Parametern, Neutrinomassen und Dunkler Materie.
    """
    
    def __init__(self, ur_params=None, num_steps=100):
        """
        Initialisiert mit Urparametern (optional) und Iterationsschritten.
        Urparameter: Dict mit E, g, sigma, Y, Phi.
        """
        self.num_steps = num_steps
        self.history = {}  # Speichert Historie pro Parameter
        
        # Standard-Urparameter (deine Werte)
        self.ur_params = ur_params or {
            'E': sp.Float(0.0063),    # Primordiale Energie
            'g': sp.Float(0.3028),    # Primordiale Kopplung
            'sigma': sp.Float(-0.2003),  # Primordiale Symmetrie
            'Y': sp.Float(0.0814),    # Yukawa-Parameter
            'Phi': sp.Float(1.0952)   # Flavor-Parameter
        }
        
        # Symbole für Emergenz
        self.E_sym, self.g_sym, self.sigma_sym, self.Y_sym, self.Phi_sym = sp.symbols('E g sigma Y Phi')
        self.init_vals = {self.E_sym: self.ur_params['E'], self.g_sym: self.ur_params['g'],
                          self.sigma_sym: self.ur_params['sigma'], self.Y_sym: self.ur_params['Y'],
                          self.Phi_sym: self.ur_params['Phi']}
        
        # Kalibrierungsfaktoren (modular anpassbar)
        self.scales = {
            'higgs': 1.98e5,           # Für ~125 GeV
            'top': 1.25e4,             # Für ~173 GeV
            'electron': 8.12e4,        # Für ~0.511 MeV
            'neutrino_normal': 1.87e6, # Für m_nu1 ~1.4 meV
            'neutrino_inverted': 2.3e7, # Für m_nu3 ~1.4 meV
            'dark_matter_fdm': 3.21e-18  # Für m_DM ~10^{-22} eV (Fuzzy DM)
        }
        
        # Neutrino-Deltas (in meV^2)
        self.delta_m21_sq = 7.5e-5 * 1e6
        self.delta_m32_sq = 2.5e-3 * 1e6
    
    def run_iteration(self):
        """Führt die iterative Rückwärtige Konvergenz durch."""
        current_E = sp.Float(0.1)  # Inhomogener Start
        current_g = sp.Float(0.5)
        current_sigma = sp.Float(-0.5)
        current_Y = sp.Float(0.2)
        current_Phi = sp.Float(2.0)
        
        self.history['E'] = [float(current_E)]
        self.history['g'] = [float(current_g)]
        self.history['sigma'] = [float(current_sigma)]
        self.history['Y'] = [float(current_Y)]
        self.history['Phi'] = [float(current_Phi)]
        
        damping = sp.exp(-abs(self.ur_params['sigma']))  # Dämpfung ~0.8187
        
        for _ in range(self.num_steps):
            current_E = damping * current_E + (1 - damping) * self.ur_params['E']
            current_g = damping * current_g + (1 - damping) * self.ur_params['g']
            current_sigma = damping * current_sigma + (1 - damping) * self.ur_params['sigma']
            current_Y = damping * current_Y + (1 - damping) * self.ur_params['Y']
            current_Phi = damping * current_Phi + (1 - damping) * self.ur_params['Phi']
            
            self.history['E'].append(float(current_E))
            self.history['g'].append(float(current_g))
            self.history['sigma'].append(float(current_sigma))
            self.history['Y'].append(float(current_Y))
            self.history['Phi'].append(float(current_Phi))
        
        # Finale Werte (SymPy für Emergenz)
        self.final_params = {
            'E': sp.Float(self.history['E'][-1]),
            'g': sp.Float(self.history['g'][-1]),
            'sigma': sp.Float(self.history['sigma'][-1]),
            'Y': sp.Float(self.history['Y'][-1]),
            'Phi': sp.Float(self.history['Phi'][-1])
        }
    
    def emerge_sm_params(self):
        """Emergenz der SM-Parameter aus finalen Urparametern."""
        final_E, final_g, final_sigma, final_Y, final_Phi = self.final_params.values()
        
        # Higgs-Masse
        m_higgs = (self.scales['higgs'] * final_E * final_g**2 * final_Phi / 
                   (1 + abs(final_sigma) * final_Y)).evalf()
        
        # Top-Quark-Masse
        m_top = (self.scales['top'] * final_Y * final_Phi * final_g**3 / 
                 abs(final_sigma)).evalf()
        
        # Feinstrukturkonstante
        alpha = (final_g**2 / (4 * sp.pi * (1 + final_sigma * final_Y))).evalf()
        
        # Cabibbo-Winkel (sin θ_C)
        theta_C_arg = abs(final_Phi * final_sigma / final_g)
        theta_C = sp.asin(theta_C_arg)
        sin_theta_C = sp.sin(theta_C).evalf()
        
        # Elektron-Masse (MeV)
        m_e = (self.scales['electron'] * final_E * final_Y**2 * abs(final_sigma)).evalf()
        
        self.sm_params = {
            'higgs_mass': float(m_higgs),
            'top_mass': float(m_top),
            'alpha': float(alpha),
            'sin_theta_C': float(sin_theta_C),
            'electron_mass': float(m_e)
        }
    
    def simulate_neutrinos(self, hierarchy='normal'):
        """Simulation der Neutrinomassen für gegebene Hierarchie."""
        final_E, final_g, final_sigma, final_Y, final_Phi = self.final_params.values()
        
        if hierarchy == 'normal':
            base_prod = final_Y**3 * final_E * abs(final_sigma) * final_Phi
            lambda_val = self.scales['neutrino_normal']
            labels = ['m_nu1', 'm_nu2', 'm_nu3']
            delta_m32_sq = self.delta_m32_sq
        else:  # inverted
            base_prod = final_Y**4 * final_E * abs(final_sigma) * final_Phi
            lambda_val = self.scales['neutrino_inverted']
            labels = ['m_nu3', 'm_nu1', 'm_nu2']
            delta_m32_sq = abs(self.delta_m32_sq)  # |Δm²₃₂| für inverted
        
        m_min = float(lambda_val * base_prod.evalf())  # in meV
        
        if hierarchy == 'normal':
            m1 = m_min
            m2 = np.sqrt(m1**2 + self.delta_m21_sq)
            m3 = np.sqrt(m2**2 + delta_m32_sq)
            masses = [m1, m2, m3]
        else:  # inverted
            m3 = m_min
            m1 = np.sqrt(m3**2 + delta_m32_sq)
            m2 = np.sqrt(m1**2 + self.delta_m21_sq)
            masses = [m3, m1, m2]
        
        self.neutrino_results = {'hierarchy': hierarchy, 'labels': labels, 'masses': masses}
    
    def simulate_dark_matter(self, model='fdm'):
        """Simulation der Dunklen Materie: Fuzzy DM Masse emergent."""
        final_E, final_g, final_sigma, final_Y, final_Phi = self.final_params.values()
        
        if model == 'fdm':
            # Fuzzy DM: Ultraleichte Skalar-Masse (10^{-22} eV)
            base_prod = final_E * final_g * abs(final_sigma) * final_Y
            scale_dm = self.scales['dark_matter_fdm']
            m_dm = float(scale_dm * base_prod.evalf())  # in eV
            self.dm_results = {'model': model, 'mass_ev': m_dm, 'description': 'Fuzzy Dark Matter Masse (ultraleicht, löst Cusp-Core-Problem)'}
        else:
            raise ValueError("Unbekanntes DM-Modell. Verwende 'fdm'.")
    
    def plot_convergence(self, save_fig=False):
        """Optionaler Plot der Konvergenz-Kurven."""
        steps = np.arange(len(self.history['E']))
        plt.figure(figsize=(10, 6))
        for param, hist in self.history.items():
            plt.plot(steps, hist, label=param)
        plt.xlabel('Iteration Steps')
        plt.ylabel('Parameter Value')
        plt.title('Konvergenz zur Primordialität')
        plt.legend()
        plt.grid(True)
        if save_fig:
            plt.savefig('figures_revers_recon_dm/convergence_plot.png')
        plt.show()
    
    def print_results(self):
        """Modulare Ausgabe aller Ergebnisse."""
        print("Urparameter nach Iteration:")
        for param, val in self.final_params.items():
            print(f"{param}: {float(val):.4f}")
        
        print("\nEmergierte SM-Parameter:")
        print(f"Higgs-Masse: {self.sm_params['higgs_mass']:.1f} GeV")
        print(f"Top-Masse: {self.sm_params['top_mass']:.1f} GeV")
        print(f"alpha: {self.sm_params['alpha']:.5f}")
        print(f"sin theta_C: {self.sm_params['sin_theta_C']:.3f}")
        print(f"Elektron-Masse: {self.sm_params['electron_mass']:.3f} MeV")
        
        # Neutrinos (beide Hierarchien)
        print("\nNormale Hierarchie Neutrinomassen (meV):")
        self.simulate_neutrinos('normal')
        for label, mass in zip(self.neutrino_results['labels'], self.neutrino_results['masses']):
            print(f"{label}: {mass:.3f}")
        
        print("\nInverted Hierarchie Neutrinomassen (meV):")
        self.simulate_neutrinos('inverted')
        for label, mass in zip(self.neutrino_results['labels'], self.neutrino_results['masses']):
            print(f"{label}: {mass:.3f}")
        
        # Dunkle Materie
        print("\nEmergierte Dunkle-Materie-Parameter (Fuzzy DM):")
        self.simulate_dark_matter('fdm')
        print(f"DM-Masse: {self.dm_results['mass_ev']:.2e} eV")
        print(f"Modell: {self.dm_results['description']}")

# Beispiel-Verwendung (modular!)
if __name__ == "__main__":
    # Instanz erstellen (optional: eigene Urparameter)
    recon = ReverseReconstruction(num_steps=100)
    
    # Iteration laufen
    recon.run_iteration()
    
    # SM-Parameter emergieren
    recon.emerge_sm_params()
    
    # Ergebnisse ausgeben
    recon.print_results()
    
    # Optional: Plot
    recon.plot_convergence(save_fig=True)
