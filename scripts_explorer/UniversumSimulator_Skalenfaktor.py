#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniversumSimulator_Skalenfaktor.py
Created on Tue Nov 18 14:04:33 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from matplotlib.patches import Circle, Rectangle

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
        self.zeit_entwicklung = []
        
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
        H_werte = self.constants['H0'] * np.sqrt(self.constants['Omega_m']/a_werte**3 + 
                                               self.constants['Omega_lambda'])
        
        ax.plot(a_werte, H_werte, 'b-', linewidth=2, label='Expansionsrate H(a)')
        ax.axvline(x=a, color='red', linestyle='--', 
                  label=f'Aktueller Skalenfaktor: {a:.2f}')
        
        # Kritische Gleichung darstellen
        omega_gesamt = self.constants['Omega_m'] + self.constants['Omega_lambda']
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
        
        ax.text(0.02, 0.95, info_text, transform=ax.transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
                fontfamily='monospace')
    
    def erstelle_stellknoepfe(self, fig):
        """Erstellt interaktive Stellknöpfe"""
        # Positionen für Slider
        slider_height = 0.03
        slider_width = 0.2
        start_x = 0.05
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
        ax_alpha = plt.axes([start_x+0.25, start_y, slider_width, slider_height])
        slider_alpha = widgets.Slider(ax_alpha, 'Feinstruktur α/α₀', 
                                    0.5, 2.0, valinit=1.0)
        
        # 5. Dunkle Energie
        ax_lambda = plt.axes([start_x+0.25, start_y-0.05, slider_width, slider_height])
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

# Zur Integration in das Hauptmenü:
def main_extended():
    print("🔬 Explorer für fundamentale Physik-Konzepte")
    print("=" * 50)
    
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
    main_extended()