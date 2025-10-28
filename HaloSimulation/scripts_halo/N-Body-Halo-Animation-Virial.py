#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N-Body-Halo-Animation-Virial.py
Created on Fri Oct 17 12:59:55 2025

@author: gh
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import njit

# -----------------------------
# Simulationseinstellungen
# -----------------------------
N = 300              # Teilchenanzahl
G = 1.0              # Gravitationskonstante (skaliert)
dt = 0.01            # Zeitschritt
steps = 1000         # Anzahl Integrationsschritte
softening = 0.05     # Softening für Stabilität
energy_interval = 20 # Energieaufzeichnungsintervall

# -----------------------------
# Virialisierte Startkonfiguration
# -----------------------------
def initialize_virialized_halo(N, G=1.0, scale=1.0, seed=42):
    np.random.seed(seed)

    # Positionen (annähernd kugelförmig verteilt)
    r = np.random.normal(0, scale, N)
    theta = np.random.uniform(0, np.pi, N)
    phi = np.random.uniform(0, 2 * np.pi, N)
    positions = np.column_stack([
        r * np.sin(theta) * np.cos(phi),
        r * np.sin(theta) * np.sin(phi),
        r * np.cos(theta)
    ])

    masses = np.ones(N)

    # Zufällige Anfangsgeschwindigkeiten
    velocities = np.random.normal(0, 0.1, (N, 3))

    # Potentielle Energie berechnen
    @njit
    def potential_energy(pos, m, G, softening):
        E_pot = 0.0
        N = len(m)
        for i in range(N):
            for j in range(i + 1, N):
                diff = pos[j] - pos[i]
                dist = np.sqrt(np.dot(diff, diff) + softening**2)
                E_pot -= G * m[i] * m[j] / dist
        return E_pot

    E_pot = potential_energy(positions, masses, G, softening)

    # Skalieren der Geschwindigkeiten nach Virialtheorem: 2E_kin + E_pot = 0
    current_E_kin = 0.5 * np.sum(masses * np.sum(velocities**2, axis=1))
    target_E_kin = -0.5 * E_pot
    scale_factor = np.sqrt(target_E_kin / current_E_kin)
    velocities *= scale_factor

    print(f"\nVirialisierte Startkonfiguration erzeugt:")
    print(f"E_pot = {E_pot:.3e}, E_kin = {target_E_kin:.3e}, Skalierung = {scale_factor:.3f}\n")

    return positions, velocities, masses


# -----------------------------
# Physikalische N-Body Dynamik
# -----------------------------
@njit
def compute_accelerations(pos, m, G, softening):
    N = len(m)
    acc = np.zeros((N, 3))
    for i in range(N):
        for j in range(N):
            if i != j:
                diff = pos[j] - pos[i]
                dist3 = (np.sqrt(np.dot(diff, diff) + softening**2))**3
                acc[i] += G * m[j] * diff / dist3
    return acc

@njit
def integrate(pos, vel, m, G, dt, softening):
    acc = compute_accelerations(pos, m, G, softening)
    vel += acc * dt / 2
    pos += vel * dt
    acc_new = compute_accelerations(pos, m, G, softening)
    vel += acc_new * dt / 2
    return pos, vel

# -----------------------------
# Hauptsimulation
# -----------------------------
positions, velocities, masses = initialize_virialized_halo(N, G)
frames = []

for step in range(steps):
    positions, velocities = integrate(positions, velocities, masses, G, dt, softening)

    # Nur jeden 10. Schritt speichern
    if step % 10 == 0:
        frames.append(positions.copy())

print("Simulation abgeschlossen – starte Animation...")

# -----------------------------
# Animation
# -----------------------------
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Virialisierter Halo – N-Body Simulation", fontsize=12)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
scat = ax.scatter([], [], [], s=5, c='cyan')

def update(frame):
    pos = frames[frame]
    scat._offsets3d = (pos[:, 0], pos[:, 1], pos[:, 2])
    ax.view_init(30, 0.3 * frame)  # langsame Rotation um z-Achse
    return scat,

ani = FuncAnimation(fig, update, frames=len(frames), interval=30, blit=False)

# --- Optional: Speichern als MP4 ---
ani.save("halo_simulation.mp4", fps=30, dpi=150)

plt.show()

