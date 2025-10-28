#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N-Body-Halo-Script_optimiz.py

Created on Fri Oct 17 12:07:56 2025

@author: gh
"""
import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange

# -----------------------------
# Parameter
# -----------------------------
G = 4.30091e-6   # Gravitationskonstante (kpc * (km/s)^2 / Msun)
N = 5000          # Teilchenanzahl
dt = 5e-4         # Zeitschritt [Gyr]
steps = 300       # Anzahl Zeitschritte
theta = 0.6       # Genauigkeit der Baum-Näherung
mass = 1e6 / N    # Masse pro Teilchen

# -----------------------------
# Anfangsbedingungen
# -----------------------------
rng = np.random.default_rng(1)
pos = rng.normal(0, 5, (N, 3)).astype(np.float64)
vel = np.zeros((N, 3), dtype=np.float64)

# -----------------------------
# Hilfsfunktionen
# -----------------------------
@njit(cache=True, parallel=True)
def compute_acc(pos, mass, theta):
    N = pos.shape[0]
    acc = np.zeros_like(pos)

    # Gitteraufbau (vereinfachter Barnes–Hut)
    grid_size = 16
    L = np.max(np.abs(pos)) + 1.0
    cell_size = 2 * L / grid_size

    mass_grid = np.zeros((grid_size, grid_size, grid_size))
    cm_grid = np.zeros((grid_size, grid_size, grid_size, 3))

    # Zell-Massen und Schwerpunkte
    for i in range(N):
        ix = int((pos[i, 0] + L) / cell_size)
        iy = int((pos[i, 1] + L) / cell_size)
        iz = int((pos[i, 2] + L) / cell_size)
        if 0 <= ix < grid_size and 0 <= iy < grid_size and 0 <= iz < grid_size:
            mass_grid[ix, iy, iz] += mass
            cm_grid[ix, iy, iz] += mass * pos[i]

    for ix in range(grid_size):
        for iy in range(grid_size):
            for iz in range(grid_size):
                m = mass_grid[ix, iy, iz]
                if m > 0:
                    cm_grid[ix, iy, iz] /= m

    # Beschleunigungen
    for i in prange(N):
        a = np.zeros(3)
        for ix in range(grid_size):
            for iy in range(grid_size):
                for iz in range(grid_size):
                    m = mass_grid[ix, iy, iz]
                    if m == 0:
                        continue
                    diff = cm_grid[ix, iy, iz] - pos[i]
                    r2 = diff[0]*diff[0] + diff[1]*diff[1] + diff[2]*diff[2] + 0.01
                    r = np.sqrt(r2)
                    s = cell_size / r
                    if s < theta:
                        a += G * m * diff / (r2 * r)
        acc[i] = a
    return acc

# -----------------------------
# Haupt-Simulationsloop
# -----------------------------
for step in range(steps):
    acc = compute_acc(pos, mass, theta)
    vel += acc * dt
    pos += vel * dt

# -----------------------------
# Plot-Ergebnis
# -----------------------------
plt.figure(figsize=(6, 6))
plt.scatter(pos[:, 0], pos[:, 1], s=0.3, alpha=0.6)
plt.title(f"Halo-Simulation (N={N}, steps={steps})")
plt.xlabel("x [kpc]")
plt.ylabel("y [kpc]")
plt.axis("equal")
plt.show()

