# -*- coding: utf-8 -*-
# physics_explorer.py*
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

def main():
    print("🔬 Explorer für fundamentale Physik-Konzepte")
    print("=" * 50)
    
    while True:
        print("\nWähle eine Simulation:")
        print("1. Mandelbrot-Menge (Mathematische Reversibilität)")
        print("2. Diskretisierte Raumzeit (LQG-Inspiriert)")
        print("3. Zellulärer Automat (Emergenz & Komplexität)")
        print("4. Beenden")
        
        choice = input("\nDeine Wahl (1-4): ").strip()
        
        if choice == '1':
            plot_mandelbrot()
        elif choice == '2':
            run_discrete_spacetime()
        elif choice == '3':
            run_cellular_automaton()
        elif choice == '4':
            print("Auf Wiedersehen! Weitere Erforschung des Universums erwartet dich!")
            break
        else:
            print("Ungültige Eingabe. Bitte wähle 1-4.")

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
    width, height = 300, 300  # Kleinere Größe für schnellere Berechnung
    
    # Erstelle Gitter
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    # Vektorisierte Berechnung der Mandelbrot-Menge
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
    
    # Einfacher Faltungskernel (ersetzt scipy.convolve)
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
        
        # Einfache "Gravitations"-Diffusion mit eigenem Convolve
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
    
    # Regel 30 - berühmt für komplexes, chaotisches Verhalten
    def rule_30(left, center, right):
        return (left & ~center & ~right) | (~left & center) | (center & ~right)
    
    # Parameter
    width = 151  # Kleinere Größe für schnellere Berechnung
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

if __name__ == "__main__":
    main()