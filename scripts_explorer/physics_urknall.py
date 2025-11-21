#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

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
    plt.show()

def run_discrete_spacetime():
    """Simuliert eine diskretisierte Raumzeit mit Quanten-Fluktuationen"""
    print("\n⏳ Starte diskretisierte Raumzeit-Simulation...")
    
    # Parameter
    grid_size = 80
    time_steps = 100
    
    # Initialisiere Raumzeit-Gitter
    spacetime = np.random.normal(0, 0.1, (grid_size, grid_size))
    
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
    
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(spacetime, cmap=cmap, vmin=-1, vmax=1, interpolation='nearest')
    ax.set_title('Diskretisierte Raumzeit mit Quanten-Fluktuationen\n(LQG-inspiriert)')
    
    def update(frame):
        nonlocal spacetime
        
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
        
        im.set_array(spacetime)
        return [im]
    
    ani = FuncAnimation(fig, update, frames=time_steps, interval=50, blit=True)
    plt.tight_layout()
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
    
    # Visualisiere das Ergebnis
    plt.figure(figsize=(12, 6))
    plt.imshow(grid, cmap='binary', interpolation='nearest')
    plt.title('Zellulärer Automat (Regel 30)\nEmergenz komplexer Muster aus einfachen Regeln')
    plt.xlabel('Raum-Dimension')
    plt.ylabel('Zeit-Dimension (nach unten)')
    plt.tight_layout()
    plt.show()

def run_discrete_spacetime_with_bigbang():
    """Simuliert eine diskretisierte Raumzeit MIT Urknall und Expansion"""
    print("\n⏳ Starte diskretisierte Raumzeit-Simulation mit Urknall...")
    
    # Parameter für die Expansion
    grid_size = 80
    total_time_steps = 200
    expansion_start = 50  # Wann beginnt die Expansion?
    
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
    
    # Spezial-Colormap für Raumzeit
    colors = ['black', 'darkblue', 'blue', 'white', 'yellow', 'red', 'darkred']
    cmap = LinearSegmentedColormap.from_list('spacetime', colors, N=256)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Raumzeit-Dichte
    im1 = ax1.imshow(spacetime, cmap=cmap, vmin=-1, vmax=1, interpolation='nearest')
    ax1.set_title('Raumzeit-Dichte und Expansion\n(Urknall → Inflation → Heute)')
    ax1.set_xlabel('Raum-Dimension X')
    ax1.set_ylabel('Raum-Dimension Y')
    
    # Plot 2: Expansions-Historie
    time_points = []
    expansion_factors = []
    line, = ax2.plot([], [], 'b-', linewidth=2)
    ax2.set_title('Kosmische Expansion')
    ax2.set_xlabel('Zeit (willkürliche Einheiten)')
    ax2.set_ylabel('Expansions-Faktor')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, total_time_steps)
    ax2.set_ylim(0, 3)
    
    # Text für kosmologische Epochen
    epoch_text = ax2.text(0.02, 0.98, '', transform=ax2.transAxes, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def get_cosmic_epoch(time_step):
        """Bestimme die kosmologische Epoche basierend auf der Zeit"""
        if time_step < 20:
            return "💥 Planck-Ära\n(Quantengravitation)"
        elif time_step < 50:
            return "⚡ Inflation\n(schnelle Expansion)"
        elif time_step < 100:
            return "🔬 Strahlungs-Ära\n(Teilchen-Entstehung)"
        elif time_step < 150:
            return "⭐ Materie-Ära\n(Sterne & Galaxien)"
        else:
            return "🌌 Dunkle Energie-Ära\n(beschleunigte Expansion)"
    
    def update(frame):
        nonlocal spacetime, time_points, expansion_factors
        
        current_epoch = get_cosmic_epoch(frame)
        
        # Expansions-Faktor basierend auf der Zeit
        if frame < expansion_start:
            # Vor der Expansion: Quantenfluktuationen dominieren
            expansion_factor = 1.0
            fluctuations_strength = 0.1
        else:
            # Nach Expansionsbeginn: Inflationäres Verhalten
            expansion_time = frame - expansion_start
            expansion_factor = 1.0 + 2.0 * (1 - np.exp(-expansion_time / 30))
            fluctuations_strength = 0.02  # Reduzierte Fluktuationen nach Expansion
        
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
        
        # Aktualisiere Plots
        im1.set_array(spacetime)
        
        # Aktualisiere Expansions-Historie
        time_points.append(frame)
        expansion_factors.append(expansion_factor)
        line.set_data(time_points, expansion_factors)
        
        # Aktualisiere Epochen-Text
        epoch_text.set_text(f'Epoche: {current_epoch}\nZeit: {frame}\nExpansion: {expansion_factor:.2f}')
        
        return [im1, line, epoch_text]
    
    ani = FuncAnimation(fig, update, frames=total_time_steps, interval=100, blit=False)
    plt.tight_layout()
    plt.show()

def main_extended():
    print("🔬 Explorer für fundamentale Physik-Konzepte")
    print("=" * 50)
    
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
    main_extended()