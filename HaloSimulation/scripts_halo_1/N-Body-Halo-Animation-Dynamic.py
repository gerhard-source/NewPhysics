#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N-Body-Halo-Animation-Dynamic.py

Created on Fri Oct 17 14:56:08 2025

@author: gh
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# -----------------------------------------
# Simulationsparameter
# -----------------------------------------
np.random.seed(42)
N = 300                 # Partikelzahl
radius = 30.0           # Startverteilung
G = 1.0                 # Grav. Konstante
dt = 0.02               # Zeitschritt
steps = 300             # Anzahl der Schritte

# -----------------------------------------
# Virialisierte Startkonfiguration
# -----------------------------------------
pos = np.random.normal(0, radius / 3, (N, 3))
r = np.linalg.norm(pos, axis=1)
sigma_v = np.sqrt(G * N / (5.0 * np.mean(r)))
vel = np.random.normal(0, sigma_v, (N, 3))
vel -= np.mean(vel, axis=0)

# -----------------------------------------
# Hilfsfunktion: Gravitationsbeschleunigung
# -----------------------------------------
def acceleration(positions):
    acc = np.zeros_like(positions)
    for i in range(N):
        diff = positions[i] - positions
        r2 = np.sum(diff**2, axis=1) + 1e-2
        inv_r3 = 1.0 / np.sqrt(r2 * r2 * r2)
        acc[i] = -G * np.sum(diff * inv_r3[:, np.newaxis], axis=0)
    return acc

# -----------------------------------------
# Simulation vorab berechnen
# -----------------------------------------
positions = []
for step in range(steps):
    acc = acceleration(pos)
    vel += acc * dt
    pos += vel * dt
    positions.append(pos.copy())

positions = np.array(positions)  # shape: (steps, N, 3)

# -----------------------------------------
# 3D-Visualisierung
# -----------------------------------------
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Dynamische N-Body-Halo-Simulation")
ax.set_xlim(-radius, radius)
ax.set_ylim(-radius, radius)
ax.set_zlim(-radius, radius)
scat = ax.scatter([], [], [], s=4, c='cyan', alpha=0.7)

# -----------------------------------------
# Kamera- und Partikelbewegung (Animation)
# -----------------------------------------
def update(frame):
    data = positions[frame]
    scat._offsets3d = (data[:, 0], data[:, 1], data[:, 2])
    # Kamera rotiert und zoomt leicht
    ax.view_init(elev=20, azim=frame)
    scale = 1.0 + 0.2 * np.sin(frame * np.pi / 90)
    ax.set_xlim(-radius * scale, radius * scale)
    ax.set_ylim(-radius * scale, radius * scale)
    ax.set_zlim(-radius * scale, radius * scale)
    return scat,

ani = FuncAnimation(fig, update, frames=steps, interval=40, blit=False)

# -----------------------------------------
# Speichern als MP4
# -----------------------------------------
ani.save("halo_dynamic.mp4", fps=25, dpi=150)
plt.close()
print("✅ Animation gespeichert als 'halo_dynamic.mp4'")

