#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Grok_physics_explorer.py
Created on Fri Oct 10 12:05:47 2025

@author: DenkRebell \ Dr.rer.nat. Gerhard Heymel
"""
import matplotlib
matplotlib.use('Qt5Agg')  # Backend für separate Plot-Fenster (funktioniert in Spyder und python3)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import convolve
import os

def main():
    print("🔬 Explorer für fundamentale Physik-Konzepte")
    print("=" * 50)
    
    # Non-interaktive Version: Führe alle Simulationen nacheinander aus
    choices = ['1', '2', '3']  # Teste alle außer Beenden
    for choice in choices:
        print(f"\n--- Simulation {choice} wird ausgeführt ---")
        if choice == '1':
            plot_mandelbrot_zoom()
        elif choice == '2':
            run_discrete_spacetime_slider()
        elif choice == '3':
            run_cellular_automaton()
    
    print("Alle Simulationen abgeschlossen!")

def plot_mandelbrot_zoom():
    """Animierter Zoom in die Mandelbrot-Menge mit GIF und Slider"""
    print("\n🎨 Berechne Mandelbrot-Zoom-Animation...")
    
    # Parameter
    width, height = 300, 300
    max_iter = 50
    time_steps = 10  # Anzahl Zoom-Schritte
    
    # Initiale View (breit)
    xmin, xmax = -2.0, 1.0
    ymin, ymax = -1.5, 1.5
    
    # Ziel-View für Zoom (Seahorse-Region)
    target_xmin, target_xmax = -0.75, -0.7
    target_ymin, target_ymax = 0.1, 0.15
    
    # Pre-berechne alle Frames
    frames = []
    for step in range(time_steps):
        # Lineare Interpolation für Zoom
        alpha = step / (time_steps - 1)
        curr_xmin = xmin + alpha * (target_xmin - xmin)
        curr_xmax = xmax + alpha * (target_xmax - xmax)
        curr_ymin = ymin + alpha * (target_ymin - ymin)
        curr_ymax = ymax + alpha * (target_ymax - ymax)
        
        x = np.linspace(curr_xmin, curr_xmax, width)
        y = np.linspace(curr_ymin, curr_ymax, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        
        mandelbrot_set = np.zeros(C.shape, dtype=int)
        z = np.zeros(C.shape, dtype=complex)
        for i in range(max_iter):
            mask = np.abs(z) <= 2
            mandelbrot_set[mask] = i
            z[mask] = z[mask]**2 + C[mask]
        frames.append(mandelbrot_set)
    
    # GIF speichern
    fig_gif, ax_gif = plt.subplots(figsize=(10, 8))
    im_gif = ax_gif.imshow(frames[0], cmap='hot', interpolation='bilinear')
    ax_gif.set_title('Mandelbrot-Zoom-Animation')
    
    def update_gif(frame):
        im_gif.set_array(frames[frame])
        return [im_gif]
    
    ani = FuncAnimation(fig_gif, update_gif, frames=time_steps, interval=200, blit=True)
    ani.save('mandelbrot_zoom.gif', writer='pillow', fps=5)
    print("Mandelbrot zoom GIF saved as 'mandelbrot_zoom.gif'")
    
    # Interaktiver Plot mit Slider
    fig_slider, ax_slider = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(bottom=0.25)
    im_slider = ax_slider.imshow(frames[0], cmap='hot', interpolation='bilinear')
    ax_slider.set_title('Mandelbrot-Zoom mit Slider (Zoom-Schritt einstellen)')
    
    # Slider
    ax_slider_pos = plt.axes([0.25, 0.1, 0.5, 0.03])
    slider = Slider(ax_slider_pos, 'Zoom-Schritt', 0, time_steps - 1, valinit=0, valfmt='%d')
    
    def update_slider(val):
        frame = int(slider.val)
        im_slider.set_array(frames[frame])
        fig_slider.canvas.draw_idle()
    
    slider.on_changed(update_slider)
    
    plt.savefig('figures_physic_explorer/mandelbrot_slider.png', dpi=100, bbox_inches='tight')  # Statischer Save
    print("Mandelbrot slider plot saved as 'mandelbrot_slider.png'")
    plt.show(block=True)  # Blockiert, bis Fenster manuell geschlossen wird
    # input("Drücke Enter zum nächsten Plot...")  # Optional: Pause aktivieren

def run_discrete_spacetime_slider():
    """Diskretisierte Raumzeit mit GIF, Slider und Zeit-Skala in Gyr"""
    print("\n⏳ Starte diskretisierte Raumzeit-Simulation mit Slider...")
    
    # Parameter
    grid_size = 80
    time_steps = 10  # Reduziert für Test
    total_age = 13.8  # Milliarden Jahre (Alter des Universums)
    
    if grid_size < 3:
        print("Grid too small for convolution! Skipping.")
        return
    
    # Initialisiere Raumzeit-Gitter und pre-berechne Frames
    spacetime = np.random.normal(0, 0.1, (grid_size, grid_size))
    kernel = np.array([[0.05, 0.1, 0.05],
                      [0.1,  0.4, 0.1],
                      [0.05, 0.1, 0.05]])
    
    frames = [spacetime.copy()]
    for step in range(1, time_steps):
        fluctuations = np.random.normal(0, 0.05, (grid_size, grid_size))
        diffused = convolve(frames[-1], kernel, mode='wrap')
        new_spacetime = 0.7 * diffused + 0.3 * fluctuations
        frames.append(new_spacetime)
    
    # Spezial-Colormap
    colors = ['darkblue', 'blue', 'white', 'red', 'darkred']
    cmap = LinearSegmentedColormap.from_list('spacetime', colors, N=256)
    
    # GIF speichern
    fig_gif, ax_gif = plt.subplots(figsize=(8, 8))
    im_gif = ax_gif.imshow(frames[0], cmap=cmap, vmin=-1, vmax=1, interpolation='nearest')
    ax_gif.set_title('Diskretisierte Raumzeit-Animation')
    
    def update_gif(frame):
        im_gif.set_array(frames[frame])
        return [im_gif]
    
    ani = FuncAnimation(fig_gif, update_gif, frames=time_steps, interval=50, blit=True)
    ani.save('spacetime.gif', writer='pillow', fps=10)
    print("Spacetime GIF saved as 'spacetime.gif'")
    
    # Interaktiver Plot mit Slider und Zeit-Label
    fig_slider, ax_slider = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(bottom=0.25)
    im_slider = ax_slider.imshow(frames[0], cmap=cmap, vmin=-1, vmax=1, interpolation='nearest')
    ax_slider.set_title('Diskretisierte Raumzeit mit Slider (LQG-inspiriert)')
    
    # Slider
    ax_slider_pos = plt.axes([0.25, 0.15, 0.5, 0.03])
    slider = Slider(ax_slider_pos, 'Zeitschritt', 0, time_steps - 1, valinit=0, valfmt='%d')
    
    # Zeit-Label unter Slider
    time_text = ax_slider.text(0.5, 0.05, f'Zeit: 0.0 Milliarden Jahre', ha='center', va='center', transform=ax_slider.transAxes)
    
    def update_slider(val):
        frame = int(slider.val)
        im_slider.set_array(frames[frame])
        # Zeit in Gyr aktualisieren
        time_gyr = (frame / (time_steps - 1)) * total_age
        time_text.set_text(f'Zeit: {time_gyr:.1f} Milliarden Jahre')
        fig_slider.canvas.draw_idle()
    
    slider.on_changed(update_slider)
    
    plt.savefig('figures_physic_explorer/spacetime_slider.png', dpi=100, bbox_inches='tight')  # Statischer Save
    print("Spacetime slider plot saved as 'spacetime_slider.png'")
    plt.show(block=True)  # Blockiert, bis Fenster manuell geschlossen wird
    # input("Drücke Enter zum nächsten Plot...")  # Optional: Pause aktivieren

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
    grid[0, width // 2] = 1
    
    print("Berechne zellulären Automaten...")
    # Wende Regel zeilenweise an (mit Randbedingungen: periodisch)
    for i in range(1, height):
        for j in range(width):
            left = grid[i-1, (j-1) % width]
            center = grid[i-1, j % width]
            right = grid[i-1, (j+1) % width]
            grid[i, j] = rule_30(left, center, right)
    
    # Visualisiere das Ergebnis, speichere und zeige in separatem Fenster an
    plt.figure(figsize=(12, 6))
    plt.imshow(grid, cmap='binary', interpolation='nearest')
    plt.title('Zellulärer Automat (Regel 30)\nEmergenz komplexer Muster aus einfachen Regeln')
    plt.xlabel('Raum-Dimension')
    plt.ylabel('Zeit-Dimension (nach unten)')
    plt.tight_layout()
    plt.savefig('figures_physic_explorer/cellular_automaton.png', dpi=100, bbox_inches='tight')
    print("Cellular automaton plot saved as 'cellular_automaton.png'")
    plt.show(block=True)  # Blockiert, bis Fenster manuell geschlossen wird
    # input("Drücke Enter zum nächsten Plot...")  # Optional: Pause aktivieren

if __name__ == "__main__":
    main()