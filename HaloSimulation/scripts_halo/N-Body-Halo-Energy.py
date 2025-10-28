#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N-Body-Halo-Energy.py
---------------------
Erweiterte Version mit Energieüberwachung zur physikalischen Kontrolle.
Nur 2 Figuren: Energieverlauf + Endzustand
Created on Fri Oct 17 12:20:40 2025

@author: gh
"""
import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # sichert korrektes Verhalten unter Ubuntu/Wayland
import matplotlib.pyplot as plt
from numba import njit

# --- Konstanten und Parameter ---
G = 1.0
N = 200
dt = 0.01
n_steps = 1000
energy_interval = 10

np.random.seed(42)
masses = np.ones(N)
positions = np.random.normal(0, 1, (N, 3))
velocities = np.random.normal(0, 0.1, (N, 3))

@njit
def compute_forces(positions, masses, G):
    N = len(masses)
    forces = np.zeros_like(positions)
    for i in range(N):
        for j in range(i + 1, N):
            diff = positions[j] - positions[i]
            dist = np.sqrt(np.dot(diff, diff)) + 1e-5
            F = G * masses[i] * masses[j] / (dist**3) * diff
            forces[i] += F
            forces[j] -= F
    return forces

@njit
def compute_energies(positions, velocities, masses, G):
    N = len(masses)
    E_kin = 0.5 * np.sum(masses * np.sum(velocities**2, axis=1))
    E_pot = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            diff = positions[j] - positions[i]
            dist = np.sqrt(np.dot(diff, diff)) + 1e-5
            E_pot -= G * masses[i] * masses[j] / dist
    return E_kin, E_pot, E_kin + E_pot

# --- Hauptintegration ---
Ekin_list, Epot_list, Etot_list = [], [], []

for step in range(n_steps):
    forces = compute_forces(positions, masses, G)
    velocities += 0.5 * forces / masses[:, None] * dt
    positions += velocities * dt
    forces_new = compute_forces(positions, masses, G)
    velocities += 0.5 * forces_new / masses[:, None] * dt

    if step % energy_interval == 0:
        E_kin, E_pot, E_tot = compute_energies(positions, velocities, masses, G)
        Ekin_list.append(E_kin)
        Epot_list.append(E_pot)
        Etot_list.append(E_tot)
        print(f"Step {step:4d}: E_kin={E_kin: .4f}, E_pot={E_pot: .4f}, E_tot={E_tot: .4f}")

# --- 1. Figur: Energieverlauf ---
plt.figure(figsize=(8, 5))
plt.plot(Ekin_list, label="E_kin", lw=1.5)
plt.plot(Epot_list, label="E_pot", lw=1.5)
plt.plot(Etot_list, label="E_tot", color='k', lw=2)
plt.xlabel("Zeitschritt / energy_interval")
plt.ylabel("Energie")
plt.legend()
plt.title("Energieerhaltung in der Halo-Simulation")
plt.tight_layout()

# --- 2. Figur: Endzustand ---
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], s=5, c='cyan', alpha=0.7)
ax.set_title("Endzustand des Halo-Systems")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.show()
