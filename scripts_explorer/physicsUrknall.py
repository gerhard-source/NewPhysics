#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
physicsUrknall.py
Created on Tue Nov 18 10:24:01 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap
import os

def plot_mandelbrot():
    """Visualisiert die Mandelbrot-Menge - reversibles mathematisches Chaos"""
    print("\n🎨 Berechne Mandelbrot-Menge...")
    
    def mandelbrot(c, max_iter=50):
        z = c
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter
    
    # Bereich für die Visualisierung
    xmin, xmax = -2.0, 1.0
    ymin, ymax = -1.5, 1.5
    width, height = 300, 300
    
    # Erstelle Gitter
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    # Vektorisierte Berechnung
    print("Berechne Iterationen...")
    mandelbrot_set = np.zeros(C.shape, dtype=int)
    z = np.zeros(C.shape, dtype=complex)
    
    for i in range(50):
        mask = np.abs(z) <= 2
        mandelbrot_set[mask] = i
        z[mask] = z[mask]**2 + C[mask]
    
    # Plotte das Ergebnis
    plt.figure(figsize=(10, 8))
    plt.imshow(mandelbrot_set, extent=[xmin, xmax, ymin, ymax], cmap='hot', interpolation='bilinear')
    plt.colorbar(label='Iterationen bis Divergenz')
    plt.title('Mandelbrot-Menge: Komplexität aus einfachen Regeln\n(z -> z² + c)')
    plt.xlabel('Realer Teil')
    plt.ylabel('Imaginärer Teil')
    
    # GIF erstellen - Zoom-Animation
    print("Erstelle Mandelbrot-GIF...")
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def animate_zoom(frame):
        # Zoom-Faktor variiert zwischen 0 und 1 und zurück
        if frame < 30:
            progress = frame / 30
            zoom_factor = 1.0 - 0.8 * progress  # Reinzoomen
        else:
            progress = (frame - 30) / 30
            zoom_factor = 0.2 + 0.8 * progress  # Rauszoomen
        
        # Berechne neuen Bereich basierend auf Zoom-Faktor
        center_x, center_y = -0.5, 0
        range_x = (xmax - xmin) * zoom_factor
        range_y = (ymax - ymin) * zoom_factor
        
        new_xmin = center_x - range_x / 2
        new_xmax = center_x + range_x / 2
        new_ymin = center_y - range_y / 2
        new_ymax = center_y + range_y / 2
        
        # Erstelle neues Gitter für diesen Zoom-Level
        x_zoom = np.linspace(new_xmin, new_xmax, width)
        y_zoom = np.linspace(new_ymin, new_ymax, height)
        X_zoom, Y_zoom = np.meshgrid(x_zoom, y_zoom)
        C_zoom = X_zoom + 1j * Y_zoom
        
        # Berechne Mandelbrot für diesen Bereich
        mandelbrot_zoom = np.zeros(C_zoom.shape, dtype=int)
        z_zoom = np.zeros(C_zoom.shape, dtype=complex)
        
        for i in range(50):
            mask = np.abs(z_zoom) <= 2
            mandelbrot_zoom[mask] = i
            z_zoom[mask] = z_zoom[mask]**2 + C_zoom[mask]
        
        ax.clear()
        ax.imshow(mandelbrot_zoom, extent=[new_xmin, new_xmax, new_ymin, new_ymax], 
                 cmap='hot', interpolation='bilinear')
        ax.set_title(f'Mandelbrot-Menge (Zoom: {zoom_factor:.2f})')
        ax.set_xlabel('Realer Teil')
        ax.set_ylabel('Imaginärer Teil')
        
        return [ax]
    
    # Erstelle GIF
    ani = FuncAnimation(fig, animate_zoom, frames=60, interval=100, blit=False)
    ani.save("mandelbrot_zoom.gif", writer=PillowWriter(fps=10))
    print("Mandelbrot-GIF gespeichert als 'mandelbrot_zoom.gif'")
    plt.close(fig)
    plt.show()

def run_discrete_spacetime():
    """Simuliert eine diskretisierte Raumzeit mit Quanten-Fluktuationen - Vor- und Rückwärts"""
    print("\n⏳ Starte diskretisierte Raumzeit-Simulation...")
    
    # Parameter
    grid_size = 80
    time_steps = 100
    
    # Initialisiere Raumzeit-Gitter
    spacetime = np.random.normal(0, 0.1, (grid_size, grid_size))
    
    # Speichere den Zustandsverlauf für Rückwärtslauf
    spacetime_history = [spacetime.copy()]
    
    # Einfacher Faltungskernel
    def simple_convolve(grid, kernel):
        result = np.zeros_like(grid)
        size = kernel.shape[0]
        offset = size // 2
        
        for i in range(offset, grid.shape[0] - offset):
            for j in range(offset, grid.shape[1] - offset):
                patch = grid[i-offset:i+offset+1, j-offset:j+offset+1]
                result[i, j] = np.sum(patch * kernel)
        return result
    
    kernel = np.array([[0.05, 0.1, 0.05],
                      [0.1,  0.4, 0.1],
                      [0.05, 0.1, 0.05]])
    
    # Spezial-Colormap für Raumzeit
    colors = ['darkblue', 'blue', 'white', 'red', 'darkred']
    cmap = LinearSegmentedColormap.from_list('spacetime', colors, N=256)
    
    # Berechne zuerst die gesamte Simulation für Vor- und Rückwärts
    print("Berechne Raumzeit-Entwicklung...")
    for frame in range(time_steps):
        # Quanten-Fluktuationen hinzufügen
        fluctuations = np.random.normal(0, 0.05, (grid_size, grid_size))
        
        # Gravitations-Diffusion
        diffused = simple_convolve(spacetime, kernel)
        spacetime = 0.7 * diffused + 0.3 * fluctuations
        
        # Periodische Randbedingungen
        spacetime[0, :] = spacetime[-2, :]
        spacetime[-1, :] = spacetime[1, :]
        spacetime[:, 0] = spacetime[:, -2]
        spacetime[:, -1] = spacetime[:, 1]
        
        spacetime_history.append(spacetime.copy())
    
    # Erstelle Animation mit Vor- und Rückwärtslauf
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(spacetime_history[0], cmap=cmap, vmin=-1, vmax=1, interpolation='nearest')
    ax.set_title('Diskretisierte Raumzeit mit Quanten-Fluktuationen\n(LQG-inspiriert)')
    
    def update(frame):
        total_frames = 2 * time_steps
        
        if frame < time_steps:
            # Vorwärts
            current_frame = frame
            direction = "▶ Vorwärts"
        else:
            # Rückwärts
            current_frame = total_frames - frame - 1
            direction = "◀ Rückwärts"
        
        im.set_array(spacetime_history[current_frame])
        ax.set_title(f'Diskretisierte Raumzeit\n{direction} - Frame {frame}/{total_frames}')
        return [im]
    
    # Erstelle GIF
    print("Erstelle Raumzeit-GIF...")
    ani = FuncAnimation(fig, update, frames=2*time_steps, interval=50, blit=True)
    ani.save("spacetime_animation.gif", writer=PillowWriter(fps=20))
    print("Raumzeit-GIF gespeichert als 'spacetime_animation.gif'")
    plt.close(fig)

def run_cellular_automaton():
    """Simuliert einen zellulären Automaten - Emergenz komplexen Verhaltens"""
    print("\n🔲 Starte zellulären Automaten (Elementar-Automat 30)...")
    
    # Regel 30
    def rule_30(left, center, right):
        return (left & ~center & ~right) | (~left & center) | (center & ~right)
    
    # Parameter
    width = 151
    height = 80
    
    # Initialisiere Gitter
    grid = np.zeros((height, width), dtype=int)
    
    # Starte mit einem einzelnen lebenden Zelle in der Mitte
    grid[0, width // 2] = 1
    
    print("Berechne zellulären Automaten...")
    # Wende Regel zeilenweise an
    for i in range(1, height):
        for j in range(1, width - 1):
            left = grid[i-1, j-1]
            center = grid[i-1, j]
            right = grid[i-1, j+1]
            grid[i, j] = rule_30(left, center, right)
    
    # Visualisiere das Ergebnis
    plt.figure(figsize=(12, 6))
    plt.imshow(grid, cmap='binary', interpolation='nearest')
    plt.title('Zellulärer Automat (Regel 30)\nEmergenz komplexer Muster aus einfachen Regeln')
    plt.xlabel('Raum-Dimension')
    plt.ylabel('Zeit-Dimension (nach unten)')
    plt.tight_layout()
    
    # Erstelle einfache GIF-Animation
    print("Erstelle Zellularautomat-GIF...")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    def animate_growth(frame):
        display_height = min(frame + 1, height)
        partial_grid = grid[:display_height, :]
        ax.clear()
        ax.imshow(partial_grid, cmap='binary', interpolation='nearest')
        ax.set_title(f'Zellulärer Automat - Wachstum ({display_height}/{height} Zeilen)')
        ax.set_xlabel('Raum-Dimension')
        ax.set_ylabel('Zeit-Dimension')
        return [ax]
    
    ani = FuncAnimation(fig, animate_growth, frames=height, interval=50, blit=False)
    ani.save("cellular_automaton.gif", writer=PillowWriter(fps=10))
    print("Zellularautomat-GIF gespeichert als 'cellular_automaton.gif'")
    plt.close(fig)
    plt.show()

def run_discrete_spacetime_with_bigbang():
    """Simuliert eine diskretisierte Raumzeit MIT Urknall und Expansion in Milliarden Jahren"""
    print("\n⏳ Starte diskretisierte Raumzeit-Simulation mit Urknall...")
    
    # Parameter für die Expansion in Milliarden Jahren
    grid_size = 80
    total_time_steps = 200
    expansion_start = 50  # Wann beginnt die Expansion?
    
    # Zeit in Milliarden Jahren seit Urknall
    def get_time_in_billion_years(time_step):
        """Konvertiert Simulationsschritte zu Milliarden Jahren"""
        if time_step < 20:
            # Sehr frühes Universum: nichtlineare Zeitskala
            return time_step * 0.001  # Erste 0.02 Milliarden Jahre
        elif time_step < 50:
            # Inflation und frühe Phase
            return 0.02 + (time_step - 20) * 0.1  # Bis ~3.2 Milliarden Jahre
        elif time_step < 100:
            # Mittlere Phase
            return 3.2 + (time_step - 50) * 0.5  # Bis ~28.2 Milliarden Jahre
        else:
            # Späte Phase
            return 28.2 + (time_step - 100) * 1.0  # Bis ~128.2 Milliarden Jahre
    
    # Initialisiere Raumzeit-Gitter - beginne mit hoher Dichte (Urknall)
    spacetime = np.zeros((grid_size, grid_size))
    
    # Urknall: Setze hohe Energie/Dichte in der Mitte
    center = grid_size // 2
    initial_radius = 5
    for i in range(grid_size):
        for j in range(grid_size):
            dist = np.sqrt((i - center)**2 + (j - center)**2)
            if dist < initial_radius:
                spacetime[i, j] = 1.0  # Hohe Anfangsdichte
    
    # Speichere Verlauf für Vor- und Rückwärts
    spacetime_history = [spacetime.copy()]
    expansion_history = [1.0]
    time_history = [0.0]
    
    # Einfacher Faltungskernel für Gravitations-Wechselwirkung
    def simple_convolve(grid, kernel):
        result = np.zeros_like(grid)
        size = kernel.shape[0]
        offset = size // 2
        
        for i in range(offset, grid.shape[0] - offset):
            for j in range(offset, grid.shape[1] - offset):
                patch = grid[i-offset:i+offset+1, j-offset:j+offset+1]
                result[i, j] = np.sum(patch * kernel)
        return result
    
    kernel = np.array([[0.05, 0.1, 0.05],
                      [0.1,  0.4, 0.1],
                      [0.05, 0.1, 0.05]])
    
    # Berechne zuerst die gesamte Simulation
    print("Berechne kosmologische Entwicklung...")
    for frame in range(1, total_time_steps + 1):
        current_time = get_time_in_billion_years(frame)
        
        # Expansions-Faktor basierend auf der Zeit
        if frame < expansion_start:
            # Vor der Expansion: Quantenfluktuationen dominieren
            expansion_factor = 1.0
            fluctuations_strength = 0.1
        else:
            # Nach Expansionsbeginn: Inflationäres Verhalten
            expansion_time = frame - expansion_start
            expansion_factor = 1.0 + 2.0 * (1 - np.exp(-expansion_time / 30))
            fluctuations_strength = 0.02
        
        # Quanten-Fluktuationen hinzufügen
        fluctuations = np.random.normal(0, fluctuations_strength, (grid_size, grid_size))
        
        # Gravitations-Diffusion
        diffused = simple_convolve(spacetime, kernel)
        
        # Kombiniere Effekte mit Expansions-Term
        if frame >= expansion_start:
            # Simuliere Expansion durch "Verdünnung"
            expansion_mask = np.ones((grid_size, grid_size))
            center = grid_size // 2
            for i in range(grid_size):
                for j in range(grid_size):
                    dist = np.sqrt((i - center)**2 + (j - center)**2)
                    # Äußere Regionen expandieren stärker
                    expansion_strength = 0.95 + 0.1 * (dist / (grid_size/2))
                    expansion_mask[i, j] = expansion_strength
            
            spacetime = 0.6 * diffused * expansion_mask + 0.4 * fluctuations
        else:
            # Vor der Expansion: Nur Gravitation und Fluktuationen
            spacetime = 0.8 * diffused + 0.2 * fluctuations
        
        # Periodische Randbedingungen
        spacetime[0, :] = spacetime[-2, :]
        spacetime[-1, :] = spacetime[1, :]
        spacetime[:, 0] = spacetime[:, -2]
        spacetime[:, -1] = spacetime[:, 1]
        
        # Speichere Zustand
        spacetime_history.append(spacetime.copy())
        expansion_history.append(expansion_factor)
        time_history.append(current_time)
    
    # Spezial-Colormap für Raumzeit
    colors = ['black', 'darkblue', 'blue', 'white', 'yellow', 'red', 'darkred']
    cmap = LinearSegmentedColormap.from_list('spacetime', colors, N=256)
    
    # Erstelle Animation mit Vor- und Rückwärts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Raumzeit-Dichte
    im1 = ax1.imshow(spacetime_history[0], cmap=cmap, vmin=-1, vmax=1, interpolation='nearest')
    ax1.set_title('Raumzeit-Dichte und Expansion\n(Urknall → Inflation → Heute)')
    ax1.set_xlabel('Raum-Dimension X')
    ax1.set_ylabel('Raum-Dimension Y')
    
    # Plot 2: Expansions-Historie
    line, = ax2.plot([], [], 'b-', linewidth=2)
    current_point, = ax2.plot([], [], 'ro', markersize=8)
    ax2.set_title('Kosmische Expansion')
    ax2.set_xlabel('Zeit (Milliarden Jahre)')
    ax2.set_ylabel('Expansions-Faktor')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, max(time_history))
    ax2.set_ylim(0, max(expansion_history) * 1.1)
    
    # Text für kosmologische Epochen
    epoch_text = ax2.text(0.02, 0.98, '', transform=ax2.transAxes, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def get_cosmic_epoch(time_step):
        """Bestimme die kosmologische Epoche basierend auf der Zeit"""
        time_billion_years = get_time_in_billion_years(time_step)
        
        if time_billion_years < 0.0001:
            return "💥 Planck-Ära\n(Quantengravitation)"
        elif time_billion_years < 0.01:
            return "⚡ Inflation\n(schnelle Expansion)"
        elif time_billion_years < 0.38:
            return "🔬 Urknall-Nukleosynthese\n(Element-Entstehung)"
        elif time_billion_years < 1:
            return "🌌 Strahlungs-Ära\n(Heißes Plasma)"
        elif time_billion_years < 10:
            return "⭐ Frühe Galaxien\n(Erste Sterne)"
        else:
            return "🌠 Heutiges Universum\n(Galaxien & Dunkle Energie)"
    
    def update(frame):
        total_frames = 2 * total_time_steps
        
        if frame < total_time_steps:
            # Vorwärts
            current_frame = frame
            direction = "▶ Vorwärts"
        else:
            # Rückwärts
            current_frame = total_frames - frame - 1
            direction = "◀ Rückwärts"
        
        current_time = time_history[current_frame]
        current_expansion = expansion_history[current_frame]
        current_epoch = get_cosmic_epoch(current_frame)
        
        # Aktualisiere Raumzeit-Plot
        im1.set_array(spacetime_history[current_frame])
        ax1.set_title(f'Raumzeit-Dichte\n{direction} - {current_time:.2f} Mrd. Jahre')
        
        # Aktualisiere Expansions-Plot
        line.set_data(time_history[:current_frame+1], expansion_history[:current_frame+1])
        current_point.set_data([current_time], [current_expansion])
        
        # Aktualisiere Epochen-Text
        epoch_text.set_text(f'Epoche: {current_epoch}\nZeit: {current_time:.2f} Mrd. Jahre\nExpansion: {current_expansion:.2f}')
        
        return [im1, line, current_point, epoch_text]
    
    # Erstelle GIF
    print("Erstelle Urknall-GIF...")
    ani = FuncAnimation(fig, update, frames=2*total_time_steps, interval=100, blit=False)
    ani.save("bigbang_animation.gif", writer=PillowWriter(fps=15))
    print("Urknall-GIF gespeichert als 'bigbang_animation.gif'")
    plt.close(fig)

def main_extended():
    print("🔬 Explorer für fundamentale Physik-Konzepte")
    print("=" * 50)
    print("✨ NEU: Vor-/Rückwärtslauf, Zeit in Milliarden Jahren, GIF-Export")
    
    while True:
        print("\nWähle eine Simulation:")
        print("1. Mandelbrot-Menge (Mathematische Reversibilität)")
        print("2. Diskretisierte Raumzeit (LQG-Inspiriert)")
        print("3. Zellulärer Automat (Emergenz & Komplexität)")
        print("4. 💥 URKNALL-Simulation (Raumzeit + Expansion)")
        print("5. Beenden")
        
        choice = input("\nDeine Wahl (1-5): ").strip()
        
        if choice == '1':
            plot_mandelbrot()
        elif choice == '2':
            run_discrete_spacetime()
        elif choice == '3':
            run_cellular_automaton()
        elif choice == '4':
            run_discrete_spacetime_with_bigbang()
        elif choice == '5':
            print("Auf Wiedersehen! Weitere Erforschung des Universums erwartet dich!")
            break
        else:
            print("Ungültige Eingabe. Bitte wähle 1-5.")

if __name__ == "__main__":
    # Erstelle Output-Verzeichnis falls nötig
    if not os.path.exists("output"):
        os.makedirs("output")
    main_extended()