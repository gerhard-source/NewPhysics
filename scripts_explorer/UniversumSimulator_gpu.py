#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniversumSimulator_gpu.py
OPTIMIERTE VERSION - Mit Performance-Verbesserungen und Status-Feedback
Created on Wed Nov 19 13:43:44 2025

@author: gh
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from matplotlib.patches import Circle
import sys
import time
from typing import List, Dict, Tuple

print("🌌 UNIVERSUM SIMULATOR - FINALE VERSION")

# GPU-Erkennung
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print("✅ CuPy verfügbar")
except:
    GPU_AVAILABLE = False
    cp = np
    print("💡 CuPy nicht verfügbar")

try:
    from numba import cuda
    NUMBA_AVAILABLE = True
    print("✅ Numba verfügbar")
except:
    NUMBA_AVAILABLE = False
    class CudaFallback:
        def jit(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
    cuda = CudaFallback()
    print("💡 Numba nicht verfügbar")

class UniversumSimulator:
    def __init__(self):
        # Physikalische Konstanten
        self.constants = {
            'G': 6.67430e-11,
            'c': 299792458, 
            'H0': 67.4,
            'Omega_m': 0.31,
            'Omega_lambda': 0.69,
            'skalenfaktor': 1.0
        }
        
        self.stern_masse = 1.0
        self.animation_running = False
        self.current_direction = 1
        self.animation_speed = 0.1
        self.expansion_history = []
        self.time_history = []
        self.praezisions_modus = False
        
        # GPU-Simulator
        self.gpu_simulator = GPUGravitationsSimulator(num_koerper=2000)
        self.letzte_simulation = None
        
        # Voreinstellungen
        self.voreinstellungen = {
            'standard': {'a': 1.0, 'G': 1.0, 'masse': 1.0, 'alpha': 1.0, 'lambda': 0.69},
            'fruehes_universum': {'a': 0.1, 'G': 1.0, 'masse': 1.0, 'alpha': 1.0, 'lambda': 0.1},
            'spaetes_universum': {'a': 2.5, 'G': 1.0, 'masse': 1.0, 'alpha': 1.0, 'lambda': 0.9},
        }

    def starte_simulation(self):
        """Startet eine GPU-Simulation"""
        print("🚀 Starte Gravitationssimulation...")
        self.letzte_simulation = self.gpu_simulator.simuliere(schritte=50)
        
        stats = self.gpu_simulator.get_stats()
        print(f"✅ Simulation abgeschlossen: {stats['kps']:,.0f} Körper/Sekunde")
        
        return self.letzte_simulation

    def berechne_stern_lebenszyklus(self):
        """Berechnet Sternenlebenszyklus"""
        masse = self.stern_masse
        
        if masse < 0.08:
            return ["Brauner Zwerg"], 1000
        elif masse < 1.4:
            return ["Hauptreihenstern", "Roter Riese", "Weisser Zwerg"], 10
        elif masse < 3.0:
            return ["Massereicher Stern", "Roter Überriese", "Supernova", "Neutronenstern"], 0.1
        else:
            return ["Hyperriese", "Supernova", "Schwarzes Loch"], 0.01

    def berechne_kosmologie(self):
        """Berechnet kosmologische Parameter"""
        a = self.constants['skalenfaktor']
        H0 = self.constants['H0']
        H = H0 * np.sqrt(self.constants['Omega_m']/a**3 + self.constants['Omega_lambda'])
        return H, 1e-26  # Vereinfachte kritische Dichte

    def visualisiere(self):
        """Hauptvisualisierung"""
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle('UNIVERSUM SIMULATOR - GPU Beschleunigt', 
                         fontsize=16, fontweight='bold', color='white')
        
        # Subplots
        self.ax_sterne = plt.axes([0.05, 0.55, 0.25, 0.35])
        self.ax_kosmologie = plt.axes([0.35, 0.55, 0.25, 0.35])
        self.ax_simulation = plt.axes([0.65, 0.55, 0.30, 0.35])
        self.ax_info = plt.axes([0.05, 0.05, 0.60, 0.4])
        self.ax_info.axis('off')
        self.ax_controls = plt.axes([0.70, 0.05, 0.25, 0.4])
        self.ax_controls.axis('off')
        
        # Initial plots
        self.update_plots()
        
        # Steuerelemente
        self.erstelle_steuerelemente()
        
        print("🎮 Simulation gestartet! Verwende die Steuerelemente.")
        plt.show()

    def update_plots(self):
        """Aktualisiert alle Plots"""
        self.plot_stern_lebenszyklus()
        self.plot_kosmologie()
        self.plot_simulation()
        self.plot_info()
        self.plot_controls_info()
        
        if hasattr(self, 'fig'):
            self.fig.canvas.draw_idle()

    def plot_stern_lebenszyklus(self):
        """Plottet Sternenlebenszyklus"""
        self.ax_sterne.clear()
        zyklus, dauer = self.berechne_stern_lebenszyklus()
        
        farben = ['blue', 'yellow', 'red', 'black', 'white']
        for i, phase in enumerate(zyklus):
            farbe = farben[i % len(farben)]
            kreis = Circle((i+1, len(zyklus)-i), 0.3, color=farbe, ec='white')
            self.ax_sterne.add_patch(kreis)
            self.ax_sterne.text(i+1, len(zyklus)-i-0.5, phase, 
                               ha='center', va='top', color='white', fontsize=8)
        
        self.ax_sterne.set_xlim(0, len(zyklus)+1)
        self.ax_sterne.set_ylim(0, len(zyklus)+1)
        self.ax_sterne.set_title(f'Sternen-Lebenszyklus\n{self.stern_masse} Sonnenmassen', 
                                color='white', fontweight='bold')
        self.ax_sterne.set_facecolor('#0f0f23')

    def plot_kosmologie(self):
        """Plottet kosmologische Entwicklung"""
        self.ax_kosmologie.clear()
        
        a_werte = np.linspace(0.1, 3, 100)
        H_werte = self.constants['H0'] * np.sqrt(
            self.constants['Omega_m']/a_werte**3 + self.constants['Omega_lambda']
        )
        
        self.ax_kosmologie.plot(a_werte, H_werte, 'cyan', linewidth=2)
        self.ax_kosmologie.axvline(x=self.constants['skalenfaktor'], color='yellow', linestyle='--')
        
        self.ax_kosmologie.set_title('Kosmologische Expansion', color='white', fontweight='bold')
        self.ax_kosmologie.set_xlabel('Skalenfaktor a', color='white')
        self.ax_kosmologie.set_ylabel('Hubble-Parameter H', color='cyan')
        self.ax_kosmologie.set_facecolor('#0f0f23')
        self.ax_kosmologie.grid(True, alpha=0.3, color='white')

    def plot_simulation(self):
        """Plottet Simulationsergebnisse"""
        self.ax_simulation.clear()
        
        if self.letzte_simulation:
            positionen = self.letzte_simulation['positionen']
            self.ax_simulation.scatter(positionen[:, 0], positionen[:, 1], 
                                     c=positionen[:, 2], cmap='viridis', 
                                     s=10, alpha=0.8)
            stats = self.gpu_simulator.get_stats()
            title = f'GPU-Simulation\n{stats["kps"]:,.0f} Körper/Sekunde'
        else:
            title = 'GPU-Simulation\nKlicke "Simulation Starten"'
            self.ax_simulation.text(0.5, 0.5, 'Noch keine Simulation\ngestartet', 
                                   ha='center', va='center', transform=self.ax_simulation.transAxes,
                                   fontsize=12, color='white')
        
        self.ax_simulation.set_title(title, color='white', fontweight='bold')
        self.ax_simulation.set_facecolor('#0f0f23')

    def plot_info(self):
        """Plottet Informationsbereich"""
        self.ax_info.clear()
        self.ax_info.axis('off')
        
        H, rho = self.berechne_kosmologie()
        zyklus, dauer = self.berechne_stern_lebenszyklus()
        stats = self.gpu_simulator.get_stats()
        
        info_text = (
            f"UNIVERSUM PARAMETER:\n"
            f"• Skalenfaktor: {self.constants['skalenfaktor']:.2f}\n"
            f"• Hubble-Parameter: {H:.1f} km/s/Mpc\n"
            f"• Materiedichte: {self.constants['Omega_m']:.2f}\n"
            f"• Dunkle Energie: {self.constants['Omega_lambda']:.2f}\n\n"
            
            f"STERNENENTWICKLUNG:\n"
            f"• Masse: {self.stern_masse:.1f} Sonnenmassen\n"
            f"• Lebensdauer: {dauer:.1f} Mrd. Jahre\n"
            f"• Phasen: {' → '.join(zyklus)}\n\n"
            
            f"SIMULATION:\n"
            f"• Modus: {stats['modus']}\n"
            f"• Performance: {stats['kps']:,.0f} Körper/Sekunde\n"
            f"• Körper: {stats['koerper']:,d}\n"
            f"• Animation: {'Läuft' if self.animation_running else 'Pausiert'}"
        )
        
        self.ax_info.text(0.65, 0.98, info_text, transform=self.ax_info.transAxes,
                         fontsize=10, color='white', va='top',
                         bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.9))

    def plot_controls_info(self):
        """Plottet Steuerungsinformationen"""
        self.ax_controls.clear()
        self.ax_controls.axis('off')
        
        controls_text = (
            "STEUERUNG:\n\n"
            "• Simulation Starten: Startet GPU-Berechnung\n"
            "• Skalenfaktor: Größe des Universums\n"
            "• Sternmasse: Masse des simulierten Sterns\n"
            "• Dunkle Energie: Anteil dunkler Energie\n\n"
            
            "SCHNELL-BUTTONS:\n"
            "• Standard: Aktuelle Parameter\n"
            "• Frühes Universum: Kleiner Skalenfaktor\n"
            "• Spätes Universum: Großer Skalenfaktor"
        )
        
        self.ax_controls.text(0.02, 0.98, controls_text, transform=self.ax_controls.transAxes,
                             fontsize=9, color='white', va='top',
                             bbox=dict(boxstyle='round', facecolor='#2a2a4e', alpha=0.8))

    def erstelle_steuerelemente(self):
        """Erstellt Steuerelemente"""
        # Slider
        slider_y = 0.45
        self.ax_slider_a = plt.axes([0.15, slider_y, 0.25, 0.02])
        self.slider_a = widgets.Slider(self.ax_slider_a, 'Skalenfaktor', 0.1, 3.0, 
                                      valinit=self.constants['skalenfaktor'])
        
        self.ax_slider_masse = plt.axes([0.15, slider_y-0.03, 0.25, 0.02])
        self.slider_masse = widgets.Slider(self.ax_slider_masse, 'Sternmasse', 0.1, 10.0,
                                          valinit=self.stern_masse)
        
        self.ax_slider_lambda = plt.axes([0.15, slider_y-0.06, 0.25, 0.02])
        self.slider_lambda = widgets.Slider(self.ax_slider_lambda, 'Dunkle Energie', 0.1, 0.9,
                                           valinit=self.constants['Omega_lambda'])
        
        # Buttons
        # Gemeinsame Stileigenschaften
        button_style = {
            'text_color': 'white',
            'font_weight': 'bold',
            'background_color': 'steelblue',
            'hover_color': 'royalblue'
            }

        button_y = 0.30
        self.ax_btn_simulation = plt.axes([0.15, button_y, 0.12, 0.04])
        self.btn_simulation = widgets.Button(self.ax_btn_simulation, 'Simulation Starten')
        self.btn_simulation.color = button_style['background_color']
        self.btn_simulation.hovercolor = button_style['hover_color']
        
        # Schnell-Buttons
        self.ax_btn_standard = plt.axes([0.28, button_y, 0.12, 0.04])
        self.btn_standard = widgets.Button(self.ax_btn_standard, 'Standard')
        
        self.ax_btn_frueh = plt.axes([0.15, button_y-0.05, 0.12, 0.04])
        self.btn_frueh = widgets.Button(self.ax_btn_frueh, 'Frühes Universum')
        
        self.ax_btn_spaet = plt.axes([0.28, button_y-0.05, 0.12, 0.04])
        self.btn_spaet = widgets.Button(self.ax_btn_spaet, 'Spätes Universum')
        
        # Callbacks
        self.slider_a.on_changed(self.update_skalenfaktor)
        self.slider_masse.on_changed(self.update_masse)
        self.slider_lambda.on_changed(self.update_lambda)
        self.btn_simulation.on_clicked(self.starte_simulation_event)
        self.btn_standard.on_clicked(lambda x: self.setze_voreinstellung('standard'))
        self.btn_frueh.on_clicked(lambda x: self.setze_voreinstellung('fruehes_universum'))
        self.btn_spaet.on_clicked(lambda x: self.setze_voreinstellung('spaetes_universum'))

    def update_skalenfaktor(self, val):
        self.constants['skalenfaktor'] = val
        self.update_plots()

    def update_masse(self, val):
        self.stern_masse = val
        self.update_plots()

    def update_lambda(self, val):
        self.constants['Omega_lambda'] = val
        self.constants['Omega_m'] = 1.0 - val
        self.update_plots()

    def starte_simulation_event(self, event):
        self.starte_simulation()
        self.update_plots()

    def setze_voreinstellung(self, name):
        if name in self.voreinstellungen:
            werte = self.voreinstellungen[name]
            self.slider_a.set_val(werte['a'])
            self.slider_masse.set_val(werte['masse'])
            self.slider_lambda.set_val(werte['lambda'])
            self.update_plots()

class GPUGravitationsSimulator:
    """GPU-beschleunigter Gravitationssimulator"""
    
    def __init__(self, num_koerper=2000):
        self.num_koerper = num_koerper
        self.performance_stats = []
        
        self.gpu_verfuegbar = GPU_AVAILABLE and NUMBA_AVAILABLE
        
        if self.gpu_verfuegbar:
            self._init_gpu()
        else:
            self._init_cpu()
    
    def _init_gpu(self):
        """GPU-Initialisierung"""
        print(f"🎮 Initialisiere GPU mit {self.num_koerper} Körpern")
        
        # Einfache Zufallsdaten
        self.positionen = cp.random.uniform(-100, 100, (self.num_koerper, 3)).astype(cp.float32)
        self.geschwindigkeiten = cp.random.normal(0, 1, (self.num_koerper, 3)).astype(cp.float32)
        self.massen = cp.ones(self.num_koerper, dtype=cp.float32) * 10.0
        
        # Gravitations-Kernel
        @cuda.jit
        def gravitation_kernel(positionen, massen, beschleunigungen, G, softening):
            i = cuda.grid(1)
            if i < positionen.shape[0]:
                ax, ay, az = 0.0, 0.0, 0.0
                for j in range(positionen.shape[0]):
                    if i != j:
                        dx = positionen[j, 0] - positionen[i, 0]
                        dy = positionen[j, 1] - positionen[i, 1]
                        dz = positionen[j, 2] - positionen[i, 2]
                        dist_sq = dx*dx + dy*dy + dz*dz + softening
                        inv_dist = 1.0 / (dist_sq ** 0.5)
                        inv_dist3 = inv_dist * inv_dist * inv_dist
                        kraft = G * massen[j] * inv_dist3
                        ax += dx * kraft
                        ay += dy * kraft
                        az += dz * kraft
                beschleunigungen[i, 0] = ax / massen[i]
                beschleunigungen[i, 1] = ay / massen[i]
                beschleunigungen[i, 2] = az / massen[i]
        
        self.kernel = gravitation_kernel
        self.gpu_modus = True
    
    def _init_cpu(self):
        """CPU-Initialisierung"""
        print(f"💻 Initialisiere CPU mit {self.num_koerper} Körpern")
        rng = np.random.RandomState(42)
        self.positionen = rng.uniform(-100, 100, (self.num_koerper, 3)).astype(np.float32)
        self.geschwindigkeiten = rng.normal(0, 1, (self.num_koerper, 3)).astype(np.float32)
        self.massen = np.ones(self.num_koerper, dtype=np.float32) * 10.0
        self.gpu_modus = False
    
    def simuliere(self, schritte=50):
        """Führt Simulation durch"""
        start_time = time.perf_counter()
        
        if self.gpu_modus:
            for _ in range(schritte):
                beschleunigungen = cp.zeros((self.num_koerper, 3), dtype=cp.float32)
                threads = 256
                blocks = (self.num_koerper + threads - 1) // threads
                self.kernel[blocks, threads](self.positionen, self.massen, beschleunigungen, 1.0, 10.0)
                self.geschwindigkeiten += beschleunigungen * 0.01
                self.positionen += self.geschwindigkeiten * 0.01
            positionen_cpu = cp.asnumpy(self.positionen)
        else:
            for _ in range(schritte):
                beschleunigungen = np.zeros((self.num_koerper, 3), dtype=np.float32)
                for i in range(self.num_koerper):
                    for j in range(self.num_koerper):
                        if i != j:
                            dx = self.positionen[j,0] - self.positionen[i,0]
                            dy = self.positionen[j,1] - self.positionen[i,1]
                            dz = self.positionen[j,2] - self.positionen[i,2]
                            dist_sq = dx*dx + dy*dy + dz*dz + 10.0
                            inv_dist = 1.0 / (dist_sq ** 0.5)
                            inv_dist3 = inv_dist * inv_dist * inv_dist
                            kraft = 1.0 * self.massen[j] * inv_dist3
                            beschleunigungen[i,0] += dx * kraft / self.massen[i]
                            beschleunigungen[i,1] += dy * kraft / self.massen[i]
                            beschleunigungen[i,2] += dz * kraft / self.massen[i]
                self.geschwindigkeiten += beschleunigungen * 0.01
                self.positionen += self.geschwindigkeiten * 0.01
            positionen_cpu = self.positionen
        
        dauer = time.perf_counter() - start_time
        kps = (self.num_koerper * schritte) / dauer if dauer > 0 else 0
        self.performance_stats.append(kps)
        
        return {'positionen': positionen_cpu, 'kps': kps}
    
    def get_stats(self):
        """Gibt Statistiken zurück"""
        if self.performance_stats:
            kps = np.mean(self.performance_stats[-5:])
        else:
            kps = 0
        
        return {
            'modus': 'GPU' if self.gpu_modus else 'CPU',
            'kps': kps,
            'koerper': self.num_koerper
        }

def main():
    """Hauptfunktion"""
    print("\n" + "🌌" * 40)
    print("UNIVERSUM SIMULATOR - GPU BESCHLEUNIGT")
    print("🌌" * 40)
    
    # Erstelle und starte Simulator
    simulator = UniversumSimulator()
    simulator.visualisiere()

if __name__ == "__main__":
    main()