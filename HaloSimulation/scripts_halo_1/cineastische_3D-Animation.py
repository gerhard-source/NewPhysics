#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cineastische_3D-Animation.py

Created on Fri Oct 17 14:51:42 2025

@author: gh
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# -----------------------------
# Parameter der Simulation
# -----------------------------
np.random.seed(42)
N = 500                 # Anzahl Partikel
radius = 50.0           # Startverteilung
G = 1.0                 # Gravitationskonstante
dt = 0.01               # Zeitschritt
steps = 500             # Simulationsschritte

# -----------------------------
# Virialisierte Startkonfiguration
# -----------------------------
pos = np.random.normal(0, radius / 3, (N, 3))  # zufällige Positionen
vel = np.zeros((N, 3))

# Berechne mittlere Entfernung zur Zentrumsmasse
r = np.linalg.norm(pos, axis=1)
sigma_v = np.sqrt(G * N / (5.0 * np.mean(r)))   # typische viriale Geschwindigkeit
vel = np.random.normal(0, sigma_v, (N, 3))      # isotrope Geschwindigkeiten

# Schwerpunktbewegung entfernen
vel -= np.mean(vel, axis=0)

# -----------------------------
# Hauptschleife der N-Body-Simulation
# (vereinfachte Gravitation für Demonstration)
# -----------------------------
for step in range(steps):
    r = np.linalg.norm(pos, axis=1).reshape(-1, 1)
    acc = -G * pos / (r**3 + 1e-3)  # weiche Gravitation
    vel += acc * dt
    pos += vel * dt

# -----------------------------
# Vorbereitung der 3D-Animation
# -----------------------------
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("3D-Halo-Simulation (virialisiert)")
ax.set_xlim(-radius, radius)
ax.set_ylim(-radius, radius)
ax.set_zlim(-radius, radius)

scat = ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], s=4, c='cyan', alpha=0.7)

# -----------------------------
# Kameraanimation: Rotation + Zoom
# -----------------------------
def update(frame):
    ax.view_init(elev=20, azim=frame)  # Kamera dreht um z-Achse
    scale = 1.0 + 0.3 * np.sin(frame * np.pi / 180)  # sanftes Ein-/Auszoomen
    ax.set_xlim(-radius * scale, radius * scale)
    ax.set_ylim(-radius * scale, radius * scale)
    ax.set_zlim(-radius * scale, radius * scale)
    return scat,

ani = FuncAnimation(fig, update, frames=360, interval=30, blit=False)

# -----------------------------
# Speichern als MP4
# -----------------------------
ani.save("halo_simulation.mp4", fps=30, dpi=150)
plt.close()
print("✅ Animation gespeichert als 'halo_simulation.mp4'")

