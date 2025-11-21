#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
physicsUniversumExplorer.py
Created on Tue Nov 18 15:41:30 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.widgets as widgets
from matplotlib.patches import Circle, Rectangle
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
    
    # Interaktive Version mit Schiebebalken
    fig, (ax, ax_slider) = plt.subplots(2, 1, figsize=(10, 10), 
                                       gridspec_kw={'height_ratios': [8, 1]})
    
    im = ax.imshow(mandelbrot_set, extent=[xmin, xmax, ymin, ymax], cmap='hot', interpolation='bilinear')
    
    # Farbskala hinzufügen
    cbar = plt.colorbar(im, ax=ax, label='Iterationen bis Divergenz')
    cbar.ax.set_ylabel('Iterationen bis Divergenz', rotation=90)
    
    ax.set_title('Mandelbrot-Menge: Komplexität aus einfachen Regeln\n(z -> z² + c)')
    ax.set_xlabel('Realer Teil')
    ax.set_ylabel('Imaginärer Teil')
    
    # Schiebebalken für Zoom
    slider_ax = plt.axes([0.2, 0.02, 0.6, 0.03])
    zoom_slider = widgets.Slider(slider_ax, 'Zoom-Faktor', 0.1, 1.0, valinit=1.0)
    
    def update_zoom(val):
        zoom_factor = zoom_slider.val
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
        
        im.set_data(mandelbrot_zoom)
        im.set_extent([new_xmin, new_xmax, new_ymin, new_ymax])
        ax.set_title(f'Mandelbrot-Menge (Zoom: {zoom_factor:.2f})')
        fig.canvas.draw_idle()
    
    zoom_slider.on_changed(update_zoom)
    
    plt.tight_layout()
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
    
    # Interaktive Version mit Schiebebalken
    fig = plt.figure(figsize=(12, 8))
    
    # Hauptplot für Raumzeit
    ax_main = plt.axes([0.1, 0.25, 0.6, 0.65])
    im = ax_main.imshow(spacetime_history[0], cmap=cmap, vmin=-1, vmax=1, interpolation='nearest')
    ax_main.set_title('Diskretisierte Raumzeit mit Quanten-Fluktuationen\n(LQG-inspiriert) - Frame 0/{}'.format(len(spacetime_history)-1))
    ax_main.set_xlabel('Raum-Dimension X')
    ax_main.set_ylabel('Raum-Dimension Y')
    
    # Farbskala
    cax = plt.axes([0.72, 0.25, 0.02, 0.65])
    cbar = plt.colorbar(im, cax=cax)
    cbar.set_label('Raumzeit-Dichte', rotation=90)
    
    # Schiebebalken
    slider_ax = plt.axes([0.1, 0.1, 0.6, 0.03])
    frame_slider = widgets.Slider(slider_ax, 'Zeitschritt', 0, len(spacetime_history)-1, valinit=0, valstep=1)
    
    # Zeit-Anzeige
    time_ax = plt.axes([0.1, 0.05, 0.6, 0.03])
    time_ax.axis('off')
    time_text = time_ax.text(0.5, 0.5, 'Richtung: Start', transform=time_ax.transAxes, 
                           ha='center', va='center', fontsize=10, 
                           bbox=dict(boxstyle='round', facecolor='lightblue'))
    
    # Verwende eine Klasse statt nonlocal
    class AnimationState:
        def __init__(self):
            self.previous_frame = 0
            self.animation_running = False
            self.current_direction = 1
    
    state = AnimationState()
    
    def update_frame(val):
        frame_idx = int(frame_slider.val)
        im.set_array(spacetime_history[frame_idx])
        
        # Bestimme Richtung
        if frame_idx == 0:
            direction = "Start"
        elif frame_idx == len(spacetime_history)-1:
            direction = "Ende"
        elif frame_idx > state.previous_frame:
            direction = "▶ Vorwärts"
        else:
            direction = "◀ Rückwärts"
        
        ax_main.set_title('Diskretisierte Raumzeit\n{} - Frame {}/{}'.format(
            direction, frame_idx, len(spacetime_history)-1))
        time_text.set_text(f'Richtung: {direction}')
        fig.canvas.draw_idle()
        
        # Aktualisiere vorherigen Frame
        state.previous_frame = frame_idx
    
    frame_slider.on_changed(update_frame)
    
    # Steuerungs-Buttons
    play_ax = plt.axes([0.8, 0.15, 0.1, 0.04])
    play_button = widgets.Button(play_ax, 'Play/Pause')
    
    reset_ax = plt.axes([0.8, 0.09, 0.1, 0.04])
    reset_button = widgets.Button(reset_ax, 'Reset')
    
    def play_pause(event):
        state.animation_running = not state.animation_running
        if state.animation_running:
            animate()
    
    def reset(event):
        frame_slider.set_val(0)
        state.previous_frame = 0
    
    def animate():
        if state.animation_running:
            current_frame = int(frame_slider.val)
            next_frame = current_frame + state.current_direction
            
            if next_frame >= len(spacetime_history) or next_frame < 0:
                state.current_direction *= -1  # Richtung umkehren
                next_frame = current_frame + state.current_direction
            
            frame_slider.set_val(next_frame)
            fig.canvas.draw_idle()
            fig.canvas.start_event_loop(0.1)
            plt.pause(0.1)
            animate()
    
    play_button.on_clicked(play_pause)
    reset_button.on_clicked(reset)
    
    plt.show()

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
    
    # Interaktive Version mit Schiebebalken
    fig = plt.figure(figsize=(14, 8))
    
    # Hauptplot
    ax_main = plt.axes([0.1, 0.25, 0.7, 0.65])
    im = ax_main.imshow(grid, cmap='binary', interpolation='nearest')
    ax_main.set_title('Zellulärer Automat (Regel 30) - Vollständige Entwicklung')
    ax_main.set_xlabel('Raum-Dimension')
    ax_main.set_ylabel('Zeit-Dimension (nach unten)')
    
    # Farbskala für binäre Werte
    cax = plt.axes([0.82, 0.25, 0.02, 0.65])
    cbar = plt.colorbar(im, cax=cax, ticks=[0, 1])
    cbar.set_ticklabels(['0 (Tot)', '1 (Lebend)'])
    cbar.set_label('Zellzustand', rotation=90)
    
    # Schiebebalken für Zeilen-Anzeige
    slider_ax = plt.axes([0.1, 0.1, 0.7, 0.03])
    row_slider = widgets.Slider(slider_ax, 'Angezeigte Zeilen', 1, height, valinit=height, valstep=1)
    
    def update_rows(val):
        rows_to_show = int(row_slider.val)
        partial_grid = grid[:rows_to_show, :]
        im.set_data(partial_grid)
        im.set_extent([0, width, rows_to_show, 0])
        ax_main.set_title(f'Zellulärer Automat (Regel 30) - Zeilen 1-{rows_to_show}')
        ax_main.set_ylim(rows_to_show, 0)
        fig.canvas.draw_idle()
    
    row_slider.on_changed(update_rows)
    
    # Erklärungs-Text
    text_ax = plt.axes([0.1, 0.02, 0.8, 0.06])
    text_ax.axis('off')
    info_text = "Regel 30: Emergenz komplexer Muster aus einfachen Regeln. " \
                "Jede Zelle wird basierend auf ihren drei Nachbarn in der vorherigen Zeile aktualisiert."
    text_ax.text(0.5, 0.5, info_text, transform=text_ax.transAxes, 
                ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightyellow'))
    
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
    
    # Interaktive Version mit Schiebebalken
    fig = plt.figure(figsize=(16, 10))
    
    # Plot 1: Raumzeit-Dichte
    ax1 = plt.axes([0.05, 0.5, 0.4, 0.4])
    im1 = ax1.imshow(spacetime_history[0], cmap=cmap, vmin=-1, vmax=1, interpolation='nearest')
    ax1.set_title('Raumzeit-Dichte\nUrknall → Expansion')
    ax1.set_xlabel('Raum-Dimension X')
    ax1.set_ylabel('Raum-Dimension Y')
    
    # Farbskala für Raumzeit
    cax1 = plt.axes([0.46, 0.5, 0.02, 0.4])
    cbar1 = plt.colorbar(im1, cax=cax1)
    cbar1.set_label('Raumzeit-Dichte', rotation=90)
    
    # Plot 2: Expansions-Historie
    ax2 = plt.axes([0.6, 0.5, 0.35, 0.4])
    line, = ax2.plot(time_history, expansion_history, 'b-', linewidth=2, alpha=0.7)
    current_point, = ax2.plot([time_history[0]], [expansion_history[0]], 'ro', markersize=8)
    ax2.set_title('Kosmische Expansion')
    ax2.set_xlabel('Zeit (Milliarden Jahre)')
    ax2.set_ylabel('Expansions-Faktor')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, max(time_history))
    ax2.set_ylim(0, max(expansion_history) * 1.1)
    
    # Epochen-Information
    epoch_ax = plt.axes([0.05, 0.25, 0.9, 0.15])
    epoch_ax.axis('off')
    
    def get_cosmic_epoch(time_step):
        """Bestimme die kosmologische Epoche basierend auf der Zeit"""
        time_billion_years = get_time_in_billion_years(time_step)
        
        if time_billion_years < 0.0001:
            return "💥 Planck-Ära", "Quantengravitation, Vereinigung aller Kräfte"
        elif time_billion_years < 0.01:
            return "⚡ Inflation", "Exponentielle Expansion, Quantenfluktuationen werden makroskopisch"
        elif time_billion_years < 0.38:
            return "🔬 Urknall-Nukleosynthese", "Entstehung der ersten Elemente (Wasserstoff, Helium)"
        elif time_billion_years < 1:
            return "🌌 Strahlungs-Ära", "Heißes Plasma, Universum undurchsichtig"
        elif time_billion_years < 10:
            return "⭐ Frühe Galaxien", "Erste Sterne und Galaxien entstehen"
        else:
            return "🌠 Heutiges Universum", "Dunkle Energie dominiert, beschleunigte Expansion"
    
    epoch_text = epoch_ax.text(0.5, 0.7, '', transform=epoch_ax.transAxes, 
                             ha='center', va='center', fontsize=12,
                             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    detail_text = epoch_ax.text(0.5, 0.3, '', transform=epoch_ax.transAxes,
                              ha='center', va='center', fontsize=10,
                              bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    # Schiebebalken
    slider_ax = plt.axes([0.1, 0.1, 0.7, 0.03])
    time_slider = widgets.Slider(slider_ax, 'Zeit (Schritte)', 0, total_time_steps, valinit=0, valstep=1)
    
    # Zeit-Anzeige
    time_display_ax = plt.axes([0.1, 0.05, 0.7, 0.03])
    time_display_ax.axis('off')
    time_display_text = time_display_ax.text(0.5, 0.5, '', transform=time_display_ax.transAxes,
                                           ha='center', va='center', fontsize=11,
                                           bbox=dict(boxstyle='round', facecolor='lightgreen'))
    
    # Animation State als Klasse
    class UrknallAnimationState:
        def __init__(self):
            self.animation_running = False
    
    anim_state = UrknallAnimationState()
    
    def update_simulation(val):
        frame_idx = int(time_slider.val)
        current_time = time_history[frame_idx]
        current_expansion = expansion_history[frame_idx]
        epoch_name, epoch_detail = get_cosmic_epoch(frame_idx)
        
        # Aktualisiere Raumzeit-Plot
        im1.set_array(spacetime_history[frame_idx])
        ax1.set_title(f'Raumzeit-Dichte\n{epoch_name} - {current_time:.3f} Mrd. Jahre')
        
        # Aktualisiere Expansions-Plot
        current_point.set_data([current_time], [current_expansion])
        
        # Aktualisiere Epochen-Text
        epoch_text.set_text(f'Epoche: {epoch_name}')
        detail_text.set_text(epoch_detail)
        
        # Aktualisiere Zeit-Anzeige
        time_display_text.set_text(
            f'Zeit: {current_time:.3f} Milliarden Jahre | '
            f'Expansion: {current_expansion:.2f}× | '
            f'Schritt: {frame_idx}/{total_time_steps}'
        )
        
        fig.canvas.draw_idle()
    
    time_slider.on_changed(update_simulation)
    
    # Steuerungs-Buttons
    button_width = 0.08
    button_height = 0.04
    button_y = 0.15
    
    play_ax = plt.axes([0.82, button_y, button_width, button_height])
    play_button = widgets.Button(play_ax, '▶ Play')
    
    pause_ax = plt.axes([0.82, button_y - 0.05, button_width, button_height])
    pause_button = widgets.Button(pause_ax, '⏸ Pause')
    
    reset_ax = plt.axes([0.82, button_y - 0.1, button_width, button_height])
    reset_button = widgets.Button(reset_ax, '⏮ Reset')
    
    def start_animation(event):
        anim_state.animation_running = True
        animate_forward()
    
    def stop_animation(event):
        anim_state.animation_running = False
    
    def reset_animation(event):
        anim_state.animation_running = False
        time_slider.set_val(0)
    
    def animate_forward():
        if anim_state.animation_running:
            current_frame = int(time_slider.val)
            next_frame = current_frame + 1
            
            if next_frame > total_time_steps:
                anim_state.animation_running = False
                return
            
            time_slider.set_val(next_frame)
            fig.canvas.draw_idle()
            plt.pause(0.05)
            animate_forward()
    
    play_button.on_clicked(start_animation)
    pause_button.on_clicked(stop_animation)
    reset_button.on_clicked(reset_animation)
    
    # Initialisiere Anzeige
    update_simulation(0)
    
    plt.tight_layout()
    plt.show()

class UniversumSimulator:
    def __init__(self):
        # Standard-Physikalische Konstanten
        self.constants = {
            'G': 6.67430e-11,      # Gravitationskonstante [m³/kg/s²]
            'c': 299792458,        # Lichtgeschwindigkeit [m/s]
            'h': 6.62607015e-34,   # Planck-Konstante [J·s]
            'alpha': 1/137.035999, # Feinstrukturkonstante
            'm_p': 1.6726219e-27,  # Protonenmasse [kg]
            'Omega_m': 0.31,       # Materiedichte-Parameter
            'Omega_lambda': 0.69,  # Dunkle Energie
            'skalenfaktor': 1.0,   # Kritischer Skalenfaktor a
            'H0': 67.4,            # Hubble-Konstante [km/s/Mpc]
        }
        
        self.stern_masse = 1.0  # Sonnenmassen
        
    def berechne_stern_lebenszyklus(self):
        """Berechnet den Lebenszyklus basierend auf aktuellen Konstanten"""
        G = self.constants['G']
        a = self.constants['skalenfaktor']
        masse = self.stern_masse
        
        # Kritische Massen skalieren mit Skalenfaktor
        masse_weißer_zwerg = 1.4 * a
        masse_neutronenstern = 3.0 * a
        masse_schwarzes_loch = 20.0 * a
        
        # Gravitationseinfluss
        grav_staerke = G / (6.67430e-11)  # Normalisiert
        
        if masse < masse_weißer_zwerg:
            zyklus = ["🔵 Hauptreihenstern", "🟡 Roter Riese", "⚪️ Weißer Zwerg"]
            dauer = 10 * grav_staerke  # Milliarden Jahre
        elif masse < masse_neutronenstern:
            zyklus = ["🔵 Massereicher Stern", "🟠 Roter Überriese", "💥 Supernova", "⚫️ Neutronenstern"]
            dauer = 0.1 * grav_staerke  # Millionen Jahre
        else:
            zyklus = ["🔵 Hyperriese", "🟠 Leuchtkräftiger Blauer Veränderlicher", "💥💥 Hypernova", "🕳️ Schwarzes Loch"]
            dauer = 0.01 * grav_staerke  # Millionen Jahre
            
        return zyklus, dauer
    
    def berechne_kosmologie(self):
        """Berechnet kosmologische Parameter basierend auf Skalenfaktor"""
        a = self.constants['skalenfaktor']
        H0 = self.constants['H0']
        
        # Friedmann-Gleichung vereinfacht
        H = H0 * np.sqrt(self.constants['Omega_m']/a**3 + self.constants['Omega_lambda'])
        
        # Kritische Dichte
        rho_crit = 3 * H**2 / (8 * np.pi * self.constants['G'])
        
        return H, rho_crit
    
    def update_simulation(self, val=None):
        """Aktualisiert die gesamte Simulation"""
        self.visualisiere_sterne_und_kosmologie()
    
    def visualisiere_sterne_und_kosmologie(self):
        """Erstellt die interaktive Visualisierung"""
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('🌌 UNIVERSUM SIMULATOR - Stellknöpfe für Physikalische Konstanten', 
                    fontsize=16, fontweight='bold')
        
        # Layout definieren
        ax_sterne = plt.axes([0.05, 0.5, 0.4, 0.4])
        ax_kosmologie = plt.axes([0.55, 0.5, 0.4, 0.4])
        ax_info = plt.axes([0.05, 0.05, 0.9, 0.35])
        ax_info.axis('off')
        
        # 1. Sternen-Lebenszyklus visualisieren
        self.plot_stern_lebenszyklus(ax_sterne)
        
        # 2. Kosmologische Parameter visualisieren
        self.plot_kosmologie(ax_kosmologie)
        
        # 3. Informationen anzeigen
        self.plot_informationen(ax_info)
        
        # 4. Stellknöpfe hinzufügen
        self.erstelle_stellknoepfe(fig)
        
        plt.show()
    
    def plot_stern_lebenszyklus(self, ax):
        """Visualisiert den Lebenszyklus von Sternen"""
        zyklus, dauer = self.berechne_stern_lebenszyklus()
        
        ax.clear()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, len(zyklus) + 1)
        
        # Lebenszyklus als Pfad darstellen
        for i, phase in enumerate(zyklus):
            # Farbige Kreise für jede Phase
            farben = {'🔵': 'blue', '🟡': 'yellow', '🟠': 'orange', 
                     '⚪️': 'white', '⚫️': 'black', '💥': 'red', '🕳️': 'darkred'}
            
            for emoji, farbe in farben.items():
                if phase.startswith(emoji):
                    kreis = Circle((i+1, len(zyklus)-i), 0.4, color=farbe, ec='black')
                    ax.add_patch(kreis)
                    ax.text(i+1, len(zyklus)-i-0.6, phase, ha='center', va='top', 
                           fontsize=9, fontweight='bold')
        
        # Verbindungslinien
        for i in range(len(zyklus)-1):
            ax.plot([i+1, i+2], [len(zyklus)-i, len(zyklus)-i-1], 'k-', alpha=0.5)
        
        ax.set_title(f'🌟 Sternen-Lebenszyklus ({self.stern_masse} Sonnenmassen)\n'
                    f'Dauer: {dauer:.2f} Zeiteinheiten', fontsize=12)
        ax.set_xlabel('Entwicklungsphasen')
        ax.set_ylabel('')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(1, len(zyklus)+1))
        ax.set_xticklabels([f'Phase {i+1}' for i in range(len(zyklus))])
    
    def plot_kosmologie(self, ax):
        """Visualisiert kosmologische Parameter"""
        H, rho_crit = self.berechne_kosmologie()
        a = self.constants['skalenfaktor']
        
        ax.clear()
        
        # Skalenfaktor vs. Expansionsrate
        a_werte = np.linspace(0.1, 3, 100)
        H_werte = self.constants['H0'] * np.sqrt(self.constants['Omega_m']/a_werte**3 + self.constants['Omega_lambda'])
        
        ax.plot(a_werte, H_werte, 'b-', linewidth=2, label='Expansionsrate H(a)')
        ax.axvline(x=a, color='red', linestyle='--', 
                  label=f'Aktueller Skalenfaktor: {a:.2f}')
        
        # Kritische Gleichung darstellen
        kritisch_werte = 1 / a_werte**2
        
        ax_twin = ax.twinx()
        ax_twin.plot(a_werte, kritisch_werte, 'g--', alpha=0.7, 
                    label='(1-Ω) ~ 1/a²')
        ax_twin.set_ylabel('Kritischer Parameter (1-Ω)', color='green')
        
        ax.set_xlabel('Skalenfaktor a')
        ax.set_ylabel('Hubble-Parameter H [km/s/Mpc]', color='blue')
        ax.set_title('Kosmologische Entwicklung\n'
                    f'Expansionsrate: {H:.1f} km/s/Mpc\n'
                    f'Kritische Dichte: {rho_crit:.2e} kg/m³', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_informationen(self, ax):
        """Zeigt detaillierte Informationen"""
        zyklus, dauer = self.berechne_stern_lebenszyklus()
        H, rho_crit = self.berechne_kosmologie()
        
        info_text = (
            f"🌌 UNIVERSUM PARAMETER:\n"
            f"• Skalenfaktor a: {self.constants['skalenfaktor']:.3f}\n"
            f"• Hubble-Konstante: {H:.1f} km/s/Mpc\n"
            f"• Kritische Dichte: {rho_crit:.2e} kg/m³\n"
            f"• Gravitationskonstante: {self.constants['G']:.2e}\n"
            f"• Feinstrukturkonstante α: {self.constants['alpha']:.6f}\n\n"
            
            f"🌟 STERNENENTWICKLUNG:\n"
            f"• Sternmasse: {self.stern_masse} Sonnenmassen\n"
            f"• Entwicklungsdauer: {dauer:.2f} Zeiteinheiten\n"
            f"• Phasen: {' → '.join(zyklus)}\n\n"
            
            f"📊 KRITISCHE GLEICHUNG:\n"
            f"(1 - Ω) = const / a² = {1/(self.constants['skalenfaktor']**2):.3f}"
        )
        
        ax.text(0.02, 0.8, info_text, transform=ax.transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
                fontfamily='monospace')

#        ax.text(0.02, 0.95, info_text, transform=ax.transAxes, fontsize=11,
#                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
#                fontfamily='monospace')

    
    def erstelle_stellknoepfe(self, fig):
        """Erstellt interaktive Stellknöpfe"""
        # Positionen für Slider
        slider_height = 0.03
        slider_width = 0.2
        start_x = 0.07
        start_y = 0.45
        
        # 1. Skalenfaktor (dein kritischer Parameter!)
        ax_skalenfaktor = plt.axes([start_x, start_y, slider_width, slider_height])
        slider_skalenfaktor = widgets.Slider(ax_skalenfaktor, 'Skalenfaktor a', 
                                           0.1, 3.0, valinit=self.constants['skalenfaktor'])
        
        # 2. Gravitationskonstante
        ax_gravitation = plt.axes([start_x, start_y-0.05, slider_width, slider_height])
        slider_gravitation = widgets.Slider(ax_gravitation, 'Gravitation G/G₀', 
                                          0.1, 2.0, valinit=1.0)
        
        # 3. Sternmasse
        ax_masse = plt.axes([start_x, start_y-0.10, slider_width, slider_height])
        slider_masse = widgets.Slider(ax_masse, 'Sternmasse [M☉]', 
                                    0.1, 50.0, valinit=self.stern_masse)
        
        # 4. Feinstrukturkonstante
        ax_alpha = plt.axes([start_x+0.32, start_y, slider_width, slider_height])
        slider_alpha = widgets.Slider(ax_alpha, 'Feinstruktur α/α₀', 
                                    0.5, 2.0, valinit=1.0)
        
        # 5. Dunkle Energie
        ax_lambda = plt.axes([start_x+0.3, start_y-0.05, slider_width, slider_height])
        slider_lambda = widgets.Slider(ax_lambda, 'Dunkle Energie Ω_Λ', 
                                     0.1, 0.9, valinit=self.constants['Omega_lambda'])
        
        # Callback-Funktionen
        def update_skalenfaktor(val):
            self.constants['skalenfaktor'] = val
            self.update_simulation()
        
        def update_gravitation(val):
            self.constants['G'] = 6.67430e-11 * val
            self.update_simulation()
        
        def update_masse(val):
            self.stern_masse = val
            self.update_simulation()
        
        def update_alpha(val):
            self.constants['alpha'] = (1/137.035999) * val
            self.update_simulation()
        
        def update_lambda(val):
            self.constants['Omega_lambda'] = val
            self.constants['Omega_m'] = 1.0 - val  # Vereinfacht
            self.update_simulation()
        
        # Verbinde Slider mit Callbacks
        slider_skalenfaktor.on_changed(update_skalenfaktor)
        slider_gravitation.on_changed(update_gravitation)
        slider_masse.on_changed(update_masse)
        slider_alpha.on_changed(update_alpha)
        slider_lambda.on_changed(update_lambda)

def starte_universum_simulator():
    """Startet den interaktiven Universum-Simulator"""
    print("🚀 Starte UNIVERSUM SIMULATOR...")
    print("🌌 Stell die fundamentalen Konstanten ein und beobachte die Konsequenzen!")
    print("⭐ Verändere den Skalenfaktor und sieh, wie sich Sternenleben und Kosmologie ändern!")
    
    simulator = UniversumSimulator()
    simulator.visualisiere_sterne_und_kosmologie()

def main_extended():
    print("🔬 Explorer für fundamentale Physik-Konzepte")
    print("=" * 50)
    print("✨ NEU: Interaktive Schiebebalken, Farbskalen, Zeitsteuerung + UNIVERSUM SIMULATOR!")
    
    while True:
        print("\nWähle eine Simulation:")
        print("1. Mandelbrot-Menge (Mathematische Reversibilität)")
        print("2. Diskretisierte Raumzeit (LQG-Inspiriert)")
        print("3. Zellulärer Automat (Emergenz & Komplexität)")
        print("4. 💥 URKNALL-Simulation (Raumzeit + Expansion)")
        print("5. 🌌 UNIVERSUM SIMULATOR (Stellknöpfe für Konstanten)")
        print("6. Beenden")
        
        choice = input("\nDeine Wahl (1-6): ").strip()
        
        if choice == '1':
            plot_mandelbrot()
        elif choice == '2':
            run_discrete_spacetime()
        elif choice == '3':
            run_cellular_automaton()
        elif choice == '4':
            run_discrete_spacetime_with_bigbang()
        elif choice == '5':
            starte_universum_simulator()
        elif choice == '6':
            print("Auf Wiedersehen! Weitere Erforschung des Universums erwartet dich!")
            break
        else:
            print("Ungültige Eingabe. Bitte wähle 1-6.")

if __name__ == "__main__":
    # Erstelle Output-Verzeichnis falls nötig
    if not os.path.exists("output"):
        os.makedirs("output")
    main_extended()