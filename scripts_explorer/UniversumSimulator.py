#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniversumSimulator.py

UNIVERSUM SIMULATOR - Standalone Version
Ein interaktiver Simulator für physikalische Konstanten und kosmologische Entwicklung
Created on Tue Nov 18 18:59:02 2025

@author: gh
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from matplotlib.patches import Circle
import sys
import os

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
        self.animation_running = False
        self.current_direction = 1  # 1 für vorwärts, -1 für rückwärts
        self.animation_speed = 0.1  # Geschwindigkeit der Animation
        self.expansion_history = []
        self.time_history = []
        
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
            zyklus = ["Hauptreihenstern", "Roter Riese", "Weisser Zwerg"]
            dauer = 10 * grav_staerke  # Milliarden Jahre
        elif masse < masse_neutronenstern:
            zyklus = ["Massereicher Stern", "Roter Überriese", "Supernova", "Neutronenstern"]
            dauer = 0.1 * grav_staerke  # Millionen Jahre
        else:
            zyklus = ["Hyperriese", "Blauer Veränderlicher", "Hypernova", "Schwarzes Loch"]
            dauer = 0.01 * grav_staerke  # Millionen Jahre
            
        return zyklus, dauer
    
    def berechne_kosmologie(self):
        """Berechnet kosmologische Parameter basierend auf Skalenfaktor"""
        a = self.constants['skalenfaktor']
        H0 = self.constants['H0']
        
        # Friedmann-Gleichung vereinfacht
        H = H0 * np.sqrt(self.constants['Omega_m']/a**3 + self.constants['Omega_lambda'])
        
        # Kritische Dichte in kg/m³
        H_si = H * 1000 / (3.086e22)  # Umrechnung in 1/s
        rho_crit = 3 * H_si**2 / (8 * np.pi * self.constants['G'])
        
        return H, rho_crit
    
    def update_simulation(self, val=None):
        """Aktualisiert die gesamte Simulation"""
        if hasattr(self, 'fig') and plt.fignum_exists(self.fig.number):
            # Aktualisiere alle Plots
            self.plot_stern_lebenszyklus(self.ax_sterne)
            self.plot_kosmologie(self.ax_kosmologie)
            self.plot_informationen(self.ax_info)
            self.plot_expansions_historie(self.ax_expansion)
            self.plot_controls_info(self.ax_controls)
            self.fig.canvas.draw_idle()
    
    def visualisiere_sterne_und_kosmologie(self):
        """Erstellt die interaktive Visualisierung"""
        # Setze Matplotlib Style für bessere Darstellung
        plt.style.use('default')
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['font.size'] = 10
        
        self.fig = plt.figure(figsize=(18, 12))
        self.fig.suptitle('UNIVERSUM SIMULATOR - Stellknöpfe für Physikalische Konstanten', 
                         fontsize=16, fontweight='bold')
        
        # Layout definieren
        self.ax_sterne = plt.axes([0.05, 0.55, 0.3, 0.35])
        self.ax_kosmologie = plt.axes([0.4, 0.55, 0.3, 0.35])
        self.ax_expansion = plt.axes([0.75, 0.55, 0.2, 0.35])
        self.ax_info = plt.axes([0.05, 0.05, 0.65, 0.4])
        self.ax_info.axis('off')
        self.ax_controls = plt.axes([0.75, 0.05, 0.2, 0.4])
        self.ax_controls.axis('off')
        
        # Erstelle alle Plots
        self.plot_stern_lebenszyklus(self.ax_sterne)
        self.plot_kosmologie(self.ax_kosmologie)
        self.plot_informationen(self.ax_info)
        self.plot_expansions_historie(self.ax_expansion)
        self.plot_controls_info(self.ax_controls)
        
        # Stellknöpfe und Steuerungs-Buttons hinzufügen
        self.erstelle_stellknoepfe(self.fig)
        self.erstelle_steuerungs_buttons(self.fig)
        
        print("Simulation gestartet! Schließen Sie das Fenster zum Beenden.")
        plt.show()
    
    def plot_stern_lebenszyklus(self, ax):
        """Visualisiert den Lebenszyklus von Sternen"""
        zyklus, dauer = self.berechne_stern_lebenszyklus()
        
        ax.clear()
        ax.set_xlim(0, len(zyklus) + 1)
        ax.set_ylim(0, len(zyklus) + 1)
        
        # Farben für jede Phase
        farben = {
            'Hauptreihenstern': 'blue', 
            'Roter Riese': 'yellow', 
            'Roter Überriese': 'orange',
            'Weisser Zwerg': 'white', 
            'Neutronenstern': 'black', 
            'Supernova': 'red', 
            'Schwarzes Loch': 'darkred',
            'Hyperriese': 'purple',
            'Blauer Veränderlicher': 'cyan',
            'Hypernova': 'darkorange'
        }
        
        # Lebenszyklus als Pfad darstellen
        for i, phase in enumerate(zyklus):
            farbe = farben.get(phase, 'gray')
            # Kreis für jede Phase
            kreis = Circle((i+1, len(zyklus)-i), 0.3, color=farbe, ec='black', zorder=3)
            ax.add_patch(kreis)
            
            # Phasentext
            ax.text(i+1, len(zyklus)-i-0.5, phase, ha='center', va='top', 
                   fontsize=8, fontweight='bold', zorder=4)
            
            # Phasennummer
            ax.text(i+1, len(zyklus)-i+0.4, f'{i+1}', ha='center', va='bottom', 
                   fontsize=10, fontweight='bold', color='darkblue')
        
        # Verbindungslinien zwischen Phasen
        for i in range(len(zyklus)-1):
            ax.plot([i+1, i+2], [len(zyklus)-i, len(zyklus)-i-1], 'k-', alpha=0.7, linewidth=2, zorder=2)
        
        ax.set_title(f'STERNEN-LEBENSZYKLUS\n{self.stern_masse} Sonnenmassen\nDauer: {dauer:.2f} Zeiteinheiten', 
                    fontsize=12, fontweight='bold', pad=20)
        ax.set_xlabel('Entwicklungsphasen')
        ax.set_ylabel('')
        ax.grid(True, alpha=0.3, zorder=1)
        ax.set_xticks(range(1, len(zyklus)+1))
        ax.set_xticklabels([f'Phase {i+1}' for i in range(len(zyklus))])
        ax.set_facecolor('#f8f9fa')
    
    def plot_kosmologie(self, ax):
        """Visualisiert kosmologische Parameter"""
        H, rho_crit = self.berechne_kosmologie()
        a = self.constants['skalenfaktor']
        
        ax.clear()
        
        # Skalenfaktor vs. Expansionsrate
        a_werte = np.linspace(0.1, 3, 100)
        H_werte = self.constants['H0'] * np.sqrt(self.constants['Omega_m']/a_werte**3 + self.constants['Omega_lambda'])
        
        # Hauptplot
        ax.plot(a_werte, H_werte, 'b-', linewidth=3, label='Expansionsrate H(a)', alpha=0.8)
        ax.axvline(x=a, color='red', linestyle='--', linewidth=2,
                  label=f'Aktueller Skalenfaktor: {a:.2f}')
        
        # Fülle den Bereich unter der Kurve
        ax.fill_between(a_werte, H_werte, alpha=0.2, color='blue')
        
        ax.set_xlabel('Skalenfaktor a', fontweight='bold')
        ax.set_ylabel('Hubble-Parameter H [km/s/Mpc]', color='blue', fontweight='bold')
        ax.set_title('KOSMOLOGISCHE ENTWICKLUNG\nExpansionsverlauf des Universums', 
                    fontsize=12, fontweight='bold')
        
        # Zweite Y-Achse für kritische Parameter
        ax2 = ax.twinx()
        kritisch_werte = 1 / a_werte**2
        ax2.plot(a_werte, kritisch_werte, 'g--', alpha=0.7, linewidth=2,
                label='Kritischer Parameter (1-Ω)')
        ax2.set_ylabel('Kritischer Parameter (1-Ω)', color='green', fontweight='bold')
        
        # Kombinierte Legende
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#f8f9fa')
        
        # Aktuelle Werte anzeigen
        ax.text(0.05, 0.95, f'Aktuelle Werte:\nH = {H:.1f} km/s/Mpc\nρ = {rho_crit:.2e} kg/m³', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    def plot_expansions_historie(self, ax):
        """Zeigt die Historie der Skalenfaktor-Änderungen"""
        ax.clear()
        
        # Füge aktuellen Wert zur Historie hinzu
        current_a = self.constants['skalenfaktor']
        current_time = len(self.time_history)
        
        self.expansion_history.append(current_a)
        self.time_history.append(current_time)
        
        # Begrenze die Historie auf 50 Einträge
        if len(self.time_history) > 50:
            self.time_history = self.time_history[-50:]
            self.expansion_history = self.expansion_history[-50:]
        
        if len(self.time_history) > 1:
            ax.plot(self.time_history, self.expansion_history, 'ro-', linewidth=2, markersize=4)
            ax.set_xlabel('Zeitschritte')
            ax.set_ylabel('Skalenfaktor a')
            ax.set_title('EXPANSIONS-HISTORIE\nVerlauf der Skalenfaktor-Änderungen', 
                        fontsize=10, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#f8f9fa')
            
            # Letzten Wert markieren
            ax.plot(self.time_history[-1], self.expansion_history[-1], 'bo', markersize=8)
        else:
            ax.text(0.5, 0.5, 'Starte Animation\num Historie zu sehen', 
                   transform=ax.transAxes, ha='center', va='center', fontsize=12,
                   bbox=dict(boxstyle='round', facecolor='lightgray'))
            ax.set_title('EXPANSIONS-HISTORIE', fontsize=10, fontweight='bold')
    
    def plot_informationen(self, ax):
        """Zeigt detaillierte Informationen"""
        zyklus, dauer = self.berechne_stern_lebenszyklus()
        H, rho_crit = self.berechne_kosmologie()
        
        info_text = (
            f"UNIVERSUM PARAMETER:\n"
            f"• Skalenfaktor a: {self.constants['skalenfaktor']:.3f}\n"
            f"• Hubble-Konstante: {H:.1f} km/s/Mpc\n"
            f"• Kritische Dichte: {rho_crit:.2e} kg/m³\n"
            f"• Gravitationskonstante: {self.constants['G']:.2e}\n"
            f"• Feinstrukturkonstante α: {self.constants['alpha']:.6f}\n"
            f"• Materiedichte Ω_m: {self.constants['Omega_m']:.3f}\n"
            f"• Dunkle Energie Ω_Λ: {self.constants['Omega_lambda']:.3f}\n\n"
            
            f"STERNENENTWICKLUNG:\n"
            f"• Sternmasse: {self.stern_masse} Sonnenmassen\n"
            f"• Entwicklungsdauer: {dauer:.2f} Zeiteinheiten\n"
            f"• Phasen: {' → '.join(zyklus)}\n\n"
            
            f"KRITISCHE GLEICHUNG:\n"
            f"(1 - Ω) = const / a² = {1/(self.constants['skalenfaktor']**2):.3f}\n\n"
            
            f"SIMULATION:\n"
            f"• Animation: {'Läuft' if self.animation_running else 'Pausiert'}\n"
            f"• Richtung: {'Vorwärts' if self.current_direction == 1 else 'Rückwärts'}\n"
            f"• Geschwindigkeit: {self.animation_speed:.1f}"
        )
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9),
                fontfamily='DejaVu Sans', linespacing=1.5)
    
    def plot_controls_info(self, ax):
        """Zeigt Informationen zur Bedienung"""
        controls_text = (
            "BEDIENUNG:\n\n"
            "STELLKNÖPFE:\n"
            "• Skalenfaktor a: Größe des Universums\n"
            "• Gravitation: Stärke der Schwerkraft\n"
            "• Sternmasse: Masse des simulierten Sterns\n"
            "• Feinstruktur: Stärke der EM-Wechselwirkung\n"
            "• Dunkle Energie: Antrieb der Expansion\n"
            "• Geschwindigkeit: Animations-Tempo\n\n"
            
            "STEUERUNG:\n"
            "• Play: Startet Animation\n"
            "• Pause: Stoppt Animation\n"
            "• Vorwärts: a vergrößern\n"
            "• Rückwärts: a verkleinern\n"
            "• Reset: Setzt alle Werte zurück"
        )
        
        ax.text(0.02, 0.98, controls_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
                fontfamily='DejaVu Sans', linespacing=1.4)
    
    def erstelle_stellknoepfe(self, fig):
        """Erstellt interaktive Stellknöpfe"""
        # Positionen für Slider
        slider_height = 0.02
        slider_width = 0.25
        start_x = 0.05
        start_y = 0.48
        
        # 1. Skalenfaktor (wichtigster Parameter!)
        ax_skalenfaktor = plt.axes([start_x, start_y, slider_width, slider_height])
        self.slider_skalenfaktor = widgets.Slider(ax_skalenfaktor, 'Skalenfaktor a', 
                                                 0.1, 3.0, valinit=self.constants['skalenfaktor'])
        
        # 2. Gravitationskonstante
        ax_gravitation = plt.axes([start_x, start_y-0.03, slider_width, slider_height])
        self.slider_gravitation = widgets.Slider(ax_gravitation, 'Gravitation G/G₀', 
                                                0.1, 2.0, valinit=1.0)
        
        # 3. Sternmasse
        ax_masse = plt.axes([start_x, start_y-0.06, slider_width, slider_height])
        self.slider_masse = widgets.Slider(ax_masse, 'Sternmasse [M☉]', 
                                         0.1, 50.0, valinit=self.stern_masse)
        
        # 4. Feinstrukturkonstante
        ax_alpha = plt.axes([start_x, start_y-0.09, slider_width, slider_height])
        self.slider_alpha = widgets.Slider(ax_alpha, 'Feinstruktur α/α₀', 
                                         0.5, 2.0, valinit=1.0)
        
        # 5. Dunkle Energie
        ax_lambda = plt.axes([start_x, start_y-0.12, slider_width, slider_height])
        self.slider_lambda = widgets.Slider(ax_lambda, 'Dunkle Energie Ω_Λ', 
                                          0.1, 0.9, valinit=self.constants['Omega_lambda'])
        
        # 6. Animationsgeschwindigkeit
        ax_speed = plt.axes([start_x, start_y-0.15, slider_width, slider_height])
        self.slider_speed = widgets.Slider(ax_speed, 'Geschwindigkeit', 
                                         0.01, 0.5, valinit=self.animation_speed)
        
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
        
        def update_speed(val):
            self.animation_speed = val
        
        # Verbinde Slider mit Callbacks
        self.slider_skalenfaktor.on_changed(update_skalenfaktor)
        self.slider_gravitation.on_changed(update_gravitation)
        self.slider_masse.on_changed(update_masse)
        self.slider_alpha.on_changed(update_alpha)
        self.slider_lambda.on_changed(update_lambda)
        self.slider_speed.on_changed(update_speed)
    
    def erstelle_steuerungs_buttons(self, fig):
        """Erstellt Play/Pause/Reset Buttons"""
        button_width = 0.1
        button_height = 0.04
        button_y = 0.35
        
        # Play Button
        play_ax = plt.axes([0.75, button_y, button_width, button_height])
        self.play_button = widgets.Button(play_ax, 'Play', color='lightgreen')
        
        # Pause Button
        pause_ax = plt.axes([0.75, button_y - 0.05, button_width, button_height])
        self.pause_button = widgets.Button(pause_ax, 'Pause', color='lightcoral')
        
        # Reset Button
        reset_ax = plt.axes([0.75, button_y - 0.10, button_width, button_height])
        self.reset_button = widgets.Button(reset_ax, 'Reset', color='lightyellow')
        
        # Vorwärts Button
        forward_ax = plt.axes([0.75, button_y + 0.06, button_width, button_height])
        self.forward_button = widgets.Button(forward_ax, 'Vorwärts')
        
        # Rückwärts Button
        backward_ax = plt.axes([0.75, button_y + 0.01, button_width, button_height])
        self.backward_button = widgets.Button(backward_ax, 'Rückwärts')
        
        # Callback-Funktionen
        def start_animation(event):
            if not self.animation_running:
                self.animation_running = True
                self.current_direction = 1
                self.animate()
        
        def start_backward_animation(event):
            if not self.animation_running:
                self.animation_running = True
                self.current_direction = -1
                self.animate()
        
        def stop_animation(event):
            self.animation_running = False
        
        def reset_animation(event):
            self.animation_running = False
            self.slider_skalenfaktor.set_val(1.0)
            self.slider_gravitation.set_val(1.0)
            self.slider_masse.set_val(1.0)
            self.slider_alpha.set_val(1.0)
            self.slider_lambda.set_val(0.69)
            self.slider_speed.set_val(0.1)
            self.expansion_history = []
            self.time_history = []
            self.update_simulation()
        
        def step_forward(event):
            current_a = self.slider_skalenfaktor.val
            new_a = min(3.0, current_a + 0.1)
            self.slider_skalenfaktor.set_val(new_a)
        
        def step_backward(event):
            current_a = self.slider_skalenfaktor.val
            new_a = max(0.1, current_a - 0.1)
            self.slider_skalenfaktor.set_val(new_a)
        
        # Verbinde Buttons mit Callbacks
        self.play_button.on_clicked(start_animation)
        self.forward_button.on_clicked(step_forward)
        self.backward_button.on_clicked(step_backward)
        self.pause_button.on_clicked(stop_animation)
        self.reset_button.on_clicked(reset_animation)
    
    def animate(self):
        """Animations-Loop für automatische Parameter-Änderung"""
        if self.animation_running and hasattr(self, 'fig') and plt.fignum_exists(self.fig.number):
            try:
                current_a = self.slider_skalenfaktor.val
                new_a = current_a + (0.05 * self.current_direction * self.animation_speed)
                
                # Begrenze den Bereich
                if new_a < 0.1:
                    new_a = 0.1
                    self.current_direction = 1  # Richtung umkehren
                elif new_a > 3.0:
                    new_a = 3.0
                    self.current_direction = -1  # Richtung umkehren
                
                self.slider_skalenfaktor.set_val(new_a)
                self.fig.canvas.draw_idle()
                plt.pause(0.05)
                self.animate()
            except (AttributeError, RuntimeError):
                # Fenster wurde geschlossen
                self.animation_running = False


def main():
    """Hauptfunktion des Universum Simulators"""
    print("=" * 60)
    print("           UNIVERSUM SIMULATOR - Standalone Version")
    print("=" * 60)
    print("Ein interaktiver Simulator für physikalische Konstanten")
    print("und kosmologische Entwicklung")
    print()
    print("Funktionen:")
    print("• 6 Stellknöpfe für fundamentale Konstanten")
    print("• Vollständige Steuerung mit Play/Pause/Reset")
    print("• Echtzeit-Visualisierung von Sternenlebenszyklen")
    print("• Kosmologische Entwicklung des Universums")
    print("• Expansions-Historie und Parameter-Tracking")
    print()
    print("Starten der Simulation...")
    print("-" * 60)
    
    try:
        # Erstelle und starte den Simulator
        simulator = UniversumSimulator()
        simulator.visualisiere_sterne_und_kosmologie()
        
        print("Simulation beendet. Auf Wiedersehen!")
        
    except KeyboardInterrupt:
        print("\nSimulation durch Benutzer abgebrochen.")
    except Exception as e:
        print(f"Fehler während der Simulation: {e}")
        print("Stellen Sie sicher, dass alle benötigten Bibliotheken installiert sind:")
        print("pip install numpy matplotlib")


if __name__ == "__main__":
    # Prüfe ob benötigte Bibliotheken vorhanden sind
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib import widgets
    except ImportError as e:
        print(f"Fehlende Bibliothek: {e}")
        print("Bitte installieren Sie die benötigten Bibliotheken:")
        print("pip install numpy matplotlib")
        sys.exit(1)
    
    # Starte das Programm
    main()
