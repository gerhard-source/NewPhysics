#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revers-Rekonstruktion

Created on Tue Oct 21 10:48:25 2025

@author: gh
"""

import sympy as sp

# Symbole und Werte
E, g, sigma, Y, Phi = sp.symbols('E g sigma Y Phi')
E_val, g_val, sigma_val, Y_val, Phi_val = 0.0063, 0.3028, -0.2003, 0.0814, 1.0952

# Ausdrücke (angepasst für Genauigkeit)
m_higgs = 10**4 * E * g**2 * Phi / (1 + sp.Abs(sigma) * Y)
m_top = 10**3 * Y * Phi * g**3 / sp.Abs(sigma)
alpha = g**2 / (4 * sp.pi * (1 + sigma * Y))
theta_C = sp.asin(Phi * sigma / g)
m_e = 10**2 * E * Y**2 * sp.Abs(sigma)  # in MeV

# Numerische Evaluation
m_higgs_num = m_higgs.subs({E: E_val, g: g_val, sigma: sigma_val, Y: Y_val, Phi: Phi_val}).evalf()
m_top_num = m_top.subs({E: E_val, g: g_val, sigma: sigma_val, Y: Y_val, Phi: Phi_val}).evalf()
alpha_num = alpha.subs({E: E_val, g: g_val, sigma: sigma_val, Y: Y_val, Phi: Phi_val}).evalf()
theta_C_sin_num = sp.sin(theta_C).subs({E: E_val, g: g_val, sigma: sigma_val, Y: Y_val, Phi: Phi_val}).evalf()
m_e_num = m_e.subs({E: E_val, g: g_val, sigma: sigma_val, Y: Y_val, Phi: Phi_val}).evalf()

# Realwerte und Genauigkeit
real_higgs, real_top, real_alpha, real_sin_theta_C, real_m_e = 125.1, 172.7, 1/137.036, 0.225, 0.511
acc_higgs = abs((float(m_higgs_num) - real_higgs) / real_higgs) * 100
# ... (ähnlich für andere)

print("Ergebnisse und Genauigkeiten:", ...)  # Wie oben