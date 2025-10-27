#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datei: Galaxie_Parameterstudie.py
Zweck: Parameterabhängigkeit der Rotationskurven im bimetrischen Modell
Autor: DenkRebell & ChatGPT (2025)
Created on Tue Oct 14 13:58:35 2025
@author: gh
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# --- optional: Arbeitsverzeichnis setzen (nur falls nötig) ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Konstanten und Grundparameter ---
G = 4.30091e-6   # (kpc * (km/s)^2) / M_sun
M_b = 6e10       # baryonische Gesamtmasse [M_sun]
r_s = 3.0        # Skalenradius [kpc]

# --- Radialgitter ---
r = np.logspace(-1, 2, 300)  # 0.1–100 kpc

# --- Funktionen ---
def M_baryon(r):
    return M_b * (1 - np.exp(-r / r_s) * (1 + r / r_s))

def phi_eff(r, alpha, r_c):
    Mb = M_baryon(r)
    return -G * Mb / r * (1 + alpha * (1 - np.exp(-r / r_c)))

def rotation_velocity(r, alpha, r_c):
    """Berechne v(r) = sqrt(r * dPhi/dr)"""
    phi = phi_eff(r, alpha, r_c)
    dphi_dr = np.gradient(phi, r)
    v = np.sqrt(np.maximum(r * (-dphi_dr), 0))
    return v

# --- Parameterarrays ---
alphas = [1, 2, 4, 8]
r_cs = [6, 12, 24]

# --- Plot vorbereiten ---
plt.figure(figsize=(8,6))

for a in alphas:
    for rc in r_cs:
        v = rotation_velocity(r, a, rc)
        plt.plot(r, v, label=fr"$\alpha={a},\,r_c={rc}$ kpc")

# --- Formatierung ---
plt.xscale('log')
plt.xlabel("Radius r [kpc]")
plt.ylabel("Rotationsgeschwindigkeit v(r) [km/s]")
plt.title("Parameterabhängigkeit der Rotationskurven im bimetrischen Modell")
plt.grid(True)
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()
