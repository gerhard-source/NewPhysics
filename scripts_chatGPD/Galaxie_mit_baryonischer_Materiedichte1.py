#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstration der effektiven Halo-Dichte im bimetrischen Modell
Created on Tue Oct 14 13:50:47 2025

@author: gh \ DenkRebell
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# Arbeitsverzeichnis automatisch setzen (Spyder-kompatibel)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Parameter (galaktisch plausibel) ---
G = 4.30091e-6   # (kpc * (km/s)^2) / M_sun
M_b = 6e10       # baryonische Gesamtmasse [M_sun]
r_s = 3.0        # Skalenradius [kpc]
alpha = 4.0      # Kopplungsstärke
r_c = 12.0       # Reichweite [kpc]

# --- Radialgitter ---
r = np.logspace(-1, 2, 300)  # 0.1–100 kpc

def M_baryon(r):
    return M_b * (1 - np.exp(-r / r_s) * (1 + r / r_s))

def phi_eff(r):
    Mb = M_baryon(r)
    return -G * Mb / r * (1 + alpha * (1 - np.exp(-r / r_c)))

# Numerische Ableitungen
dphi_dr = np.gradient(phi_eff(r), r)
dphi_dr[dphi_dr > 0] = 0  # unphysikalische Repulsion unterdrücken

v = np.sqrt(np.maximum(r * (-dphi_dr), 0))
rho_eff = (1 / (4 * np.pi * G * r**2)) * np.gradient(r**2 * dphi_dr, r)

# --- Plots ---
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(r, v, label="Gesamt (bimetric)")
ax[0].plot(r, np.sqrt(G * M_baryon(r) / r), '--', label="Nur baryonisch")
ax[0].set_xscale('log')
ax[0].set_xlabel("Radius r [kpc]")
ax[0].set_ylabel("v(r) [km/s]")
ax[0].legend()
ax[0].grid(True)
ax[0].set_title("Rotationskurven")

ax[1].loglog(r, np.abs(rho_eff), label=r"$\rho_\mathrm{eff}(r)$")
ax[1].set_xlabel("Radius r [kpc]")
ax[1].set_ylabel(r"Dichte [M$_\odot$/kpc$^3$]")
ax[1].grid(True)
ax[1].set_title("Effektive Halo-Dichte")
ax[1].legend()

plt.tight_layout()
plt.show()

