#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N-Body-Halo-Animation.py
------------------------
3D-animierte Halo-Simulation (interaktiv mit matplotlib.FuncAnimation)
Rotation um die z-Achse + Energieerhaltungskontrolle

Benötigte Pakete:
numpy<2, scipy<1.12, matplotlib>=3.7,<3.9, numba<0.59

Created on Fri Oct 17 12:47:33 2025

@author: gh
"""

import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # wichtig unter Ubuntu/Wayland
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import njit

# --- Parameter ---
G = 1.0
N = 200
dt = 0.01
steps = 500

np.random.seed(42)
masses = np.ones(N)
positions = np.random.normal(0, 1, (N, 3))
velocities = np.random.normal(0, 0.1, (N, 3))

@njit
def compute_forces(pos, m, G):
    N = len(m)
    F = np.zeros_like(pos)
    for i in range(N):
        for j in range(i + 1, N):
            diff = pos[j] - pos[i]
            dist = np.sqrt(np.dot(diff, diff)) + 1e-5
            f = G * m[i] * m[j] / (dist**3) * diff
            F[i] += f
            F[j] -= f
    return F

@njit
def step_system(pos, vel, m, G, dt):
    F = compute_forces(pos, m, G)
    vel += 0.5 * F / m[:, None] * dt
    pos += vel * dt
    F2 = compute_forces(pos, m, G)
    vel += 0.5 * F2 / m[:, None] * dt
    return pos, vel

# --- Animation vorbereiten ---
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)
scat = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], s=10, c='cyan', alpha=0.7)
ax.set_title("Halo-Entwicklung (3D)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

def update(frame):
    global positions, velocities
    positions, velocities = step_system(positions, velocities, masses, G, dt)
    scat._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])
    ax.view_init(30, frame % 360)  # Drehung um z-Achse
    return scat,

ani = FuncAnimation(fig, update, frames=steps, interval=30, blit=False)
plt.tight_layout()
plt.show()

