#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Reverse-Rekonstruktion-Iteration.py

Created on Tue Oct 21 11:02:23 2025

@author: gh
"""

import sympy as sp
import numpy as np

# Symbole und Urwerte
E_sym, g_sym, sigma_sym, Y_sym, Phi_sym = sp.symbols('E g sigma Y Phi')
init_vals = {E_sym: sp.Float(0.0063), g_sym: sp.Float(0.3028), sigma_sym: sp.Float(-0.2003), 
             Y_sym: sp.Float(0.0814), Phi_sym: sp.Float(1.0952)}

def iterative_reconstruction(num_steps=100):
    current_E = sp.Float(0.1)  # Inhomogener Start
    current_g = sp.Float(0.5)
    current_sigma = sp.Float(-0.5)
    current_Y = sp.Float(0.2)
    current_Phi = sp.Float(2.0)
    
    history_E, history_g, history_sigma, history_Y, history_Phi = [float(current_E)], [float(current_g)], [float(current_sigma)], [float(current_Y)], [float(current_Phi)]
    
    damping = sp.exp(-abs(init_vals[sigma_sym]))  # ≈0.8187
    
    for _ in range(num_steps):
        current_E = damping * current_E + (1 - damping) * init_vals[E_sym]
        current_g = damping * current_g + (1 - damping) * init_vals[g_sym]
        current_sigma = damping * current_sigma + (1 - damping) * init_vals[sigma_sym]
        current_Y = damping * current_Y + (1 - damping) * init_vals[Y_sym]
        current_Phi = damping * current_Phi + (1 - damping) * init_vals[Phi_sym]
        
        history_E.append(float(current_E))
        history_g.append(float(current_g))
        history_sigma.append(float(current_sigma))
        history_Y.append(float(current_Y))
        history_Phi.append(float(current_Phi))
    
    return np.array(history_E), np.array(history_g), np.array(history_sigma), np.array(history_Y), np.array(history_Phi)

# Ausführung und Emergenz (mit Kalibrierung für sin θ_C: abs(sigma))
hist_E, hist_g, hist_sigma, hist_Y, hist_Phi = iterative_reconstruction()
final_E, final_g, final_sigma, final_Y, final_Phi = sp.Float(hist_E[-1]), sp.Float(hist_g[-1]), sp.Float(hist_sigma[-1]), sp.Float(hist_Y[-1]), sp.Float(hist_Phi[-1])

# Kalibrierte Formeln (angepasst für Übereinstimmung)
scale_h = 1.98e4  # Kalib. Faktor für Higgs (Beispiel)
m_higgs = (scale_h * final_E * final_g**2 * final_Phi / (1 + abs(final_sigma) * final_Y)).evalf()
# Ähnlich für andere...

print(f"Konvergiert: E={hist_E[-1]:.4f} | Higgs: {float(m_higgs):.1f} GeV")