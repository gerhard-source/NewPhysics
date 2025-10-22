# -*- coding: utf-8 -*-
""" Galaxie_mit_baryonischer_Materiedichte.py
Dat: 14.10.25
Autor: DenkRebell

"""
import numpy as np
import matplotlib.pyplot as plt

# --- Parameter ---
G = 4.30091e-6   # (kpc * (km/s)^2) / M_sun
M_b = 6e10       # M_sun
r_s = 3.0        # kpc
alpha = 4.0
r_c = 12.0       # kpc

r = np.logspace(-1, 2, 300)

def M_baryon(r):
    return M_b * (1 - np.exp(-r / r_s) * (1 + r / r_s))

def phi_eff(r):
    Mb = M_baryon(r)
    return -G * Mb / r * (1 + alpha * (1 - np.exp(-r / r_c)))

# Numerische Ableitungen
dphi_dr = np.gradient(phi_eff(r), r)

# --- Physikalische Korrektur ---
# Wenn Ableitung positiv (unphysikalisch), auf Null setzen
dphi_dr[dphi_dr > 0] = 0

v = np.sqrt(np.maximum(r * (-dphi_dr), 0))  # negativ, aber positiv multipliziert
rho_eff = (1 / (4 * np.pi * G * r**2)) * np.gradient(r**2 * dphi_dr, r)

# --- Plot ---
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
