#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/physik/scripts/quark_gluon_couplings.py
import numpy as np
import matplotlib.pyplot as plt

class QuarkGluonCouplings:
    def __init__(self):
        # DEINE 5 primordiale Parameter
        self.primordial_params = {
            'E': 0.0063,      # Primordial Energy
            'g': 0.3028,      # Primordial Coupling  
            'S': -0.2003,     # Primordial Symmetry
            'Y': 0.0814,      # Yukawa Parameter
            'Φ': 1.0952       # Flavor Parameter
        }
        
        # Bekannte Lepton-Kopplungen (aus deiner Analyse)
        self.known_lepton_couplings = {
            'electron': 0.00024,
            'muon': 0.00024,
            'tau': 0.00018
        }
    
    def calculate_dilaton_couplings(self):
        """Berechnet Dilaton-artige Kopplungen basierend auf Standardmodell-Beta-Funktionen"""
        
        # Basierend auf deinen Parametern:
        base_coupling = self.primordial_params['Y']  # Yukawa-basiert
        
        # Quark-Kopplungen (masse-proportional wie bei Dilaton)
        quark_masses_mev = {
            'up': 2.2, 'down': 4.7, 'charm': 1270, 
            'strange': 93, 'top': 172000, 'bottom': 4180
        }
        
        # Normierung auf Top-Quark (stärkste Kopplung)
        max_quark_mass = max(quark_masses_mev.values())
        
        quark_couplings = {}
        for quark, mass in quark_masses_mev.items():
            # Masse-proportionale Kopplung + Flavor-Faktor aus Φ
            coupling = (base_coupling * (mass / max_quark_mass) * 
                       self.primordial_params['Φ'])
            quark_couplings[quark] = coupling
        
        # Gluon-Kopplung (stark wegen QCD Beta-Funktion)
        # β_QCD ≈ 7 - typisch groß
        qcd_beta_function = 7.0
        gluon_coupling = (self.primordial_params['g'] * qcd_beta_function * 
                         self.primordial_params['E'])
        
        # Photon-Kopplung (QED Beta-Funktion ist klein)
        qed_beta_function = -0.3  # Negativ für U(1)
        photon_coupling = (self.primordial_params['g'] * abs(qed_beta_function) * 
                          self.primordial_params['E'])
        
        return {
            'quarks': quark_couplings,
            'gluons': gluon_coupling,
            'photons': photon_coupling
        }
    
    def calculate_branching_ratios(self, couplings):
        """Berechnet Zerfallsverhältnisse basierend auf Kopplungen"""
        
        # Für skalares Teilchen bei 1000 GeV
        mass = 1000.0  # GeV
        
        # Phase space Faktoren (vereinfacht)
        phase_space = {
            'leptons': 1.0,      # e⁺e⁻, μ⁺μ⁻, τ⁺τ⁻
            'quarks': 3.0,       # Farbfaktor
            'gluons': 8.0,       # 8 Gluonen
            'photons': 1.0
        }
        
        # Berechne partielle Zerfallsbreiten
        partial_widths = {}
        
        # Lepton-Zerfälle (bekannt aus deiner Analyse)
        lepton_width = sum([c**2 for c in self.known_lepton_couplings.values()]) * phase_space['leptons']
        partial_widths['leptons'] = lepton_width
        
        # Quark-Zerfälle
        quark_width = sum([c**2 for c in couplings['quarks'].values()]) * phase_space['quarks']
        partial_widths['quarks'] = quark_width
        
        # Gluon-Zerfall
        gluon_width = couplings['gluons']**2 * phase_space['gluons']
        partial_widths['gluons'] = gluon_width
        
        # Photon-Zerfall  
        photon_width = couplings['photons']**2 * phase_space['photons']
        partial_widths['photons'] = photon_width
        
        # Total width
        total_width = sum(partial_widths.values())
        
        # Branching ratios
        branching_ratios = {channel: width/total_width for channel, width in partial_widths.items()}
        
        return branching_ratios, partial_widths, total_width

    def plot_coupling_comparison(self, calculated_couplings):
        """Plottet den Vergleich der Kopplungsstärken"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Fermion-Kopplungen
        fermions = list(self.known_lepton_couplings.keys()) + list(calculated_couplings['quarks'].keys())
        couplings = list(self.known_lepton_couplings.values()) + list(calculated_couplings['quarks'].values())
        colors = ['red']*3 + ['blue']*6  # 3 Leptons rot, 6 Quarks blau
        
        bars = ax1.bar(fermions, couplings, color=colors, alpha=0.7)
        ax1.set_ylabel('Kopplungsstärke')
        ax1.set_title('Vergleich: Lepton- vs Quark-Kopplungen')
        ax1.tick_params(axis='x', rotation=45)
        ax1.set_yscale('log')  # Logarithmisch wegen großer Variation
        
        # Werte anzeigen
        for i, (bar, coupling) in enumerate(zip(bars, couplings)):
            if coupling > 0.0001:  # Nur sinnvolle Werte anzeigen
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                        f'{coupling:.1e}', ha='center', va='bottom', fontsize=8)
        
        # Plot 2: Boson-Kopplungen
        bosons = ['Gluonen', 'Photonen']
        boson_couplings = [calculated_couplings['gluons'], calculated_couplings['photons']]
        bars2 = ax2.bar(bosons, boson_couplings, color=['orange', 'green'], alpha=0.7)
        ax2.set_ylabel('Kopplungsstärke')
        ax2.set_title('Eichboson-Kopplungen')
        
        # Werte anzeigen
        for bar, coupling in zip(bars2, boson_couplings):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{coupling:.1e}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('../results/coupling_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()

# Berechnung durchführen
print("🚀 BERECHNUNG DER QUARK/GLUON-KOPPLUNGEN...")
coupling_calculator = QuarkGluonCouplings()
calculated_couplings = coupling_calculator.calculate_dilaton_couplings()
branching_ratios, partial_widths, total_width = coupling_calculator.calculate_branching_ratios(calculated_couplings)

print("\n" + "="*60)
print("🔬 BERECHNETE QUARK/GLUON-KOPPLUNGEN")
print("="*60)

print("\n📊 QUARK-KOPPLUNGEN:")
for quark, coupling in calculated_couplings['quarks'].items():
    print(f"   {quark:8}: {coupling:.2e}")

print(f"\n📊 GLUON-KOPPLUNG:  {calculated_couplings['gluons']:.2e}")
print(f"📊 PHOTON-KOPPLUNG: {calculated_couplings['photons']:.2e}")

print(f"\n📊 BEKANNTE LEPTON-KOPPLUNGEN:")
for lepton, coupling in coupling_calculator.known_lepton_couplings.items():
    print(f"   {lepton:8}: {coupling:.2e}")

print("\n" + "="*60)
print("🎯 VORHERSAGE FÜR ZERFALLSVERHÄLTNISSE")
print("="*60)

for channel, ratio in branching_ratios.items():
    print(f"   {channel:8}: {ratio*100:6.2f}%")

print(f"\n📈 GESAMTBREITE: {total_width:.2e}")
print(f"📈 MESSBARE BREITE: ~{total_width * 1000:.1f} MeV")  # Umrechnung GeV → MeV

print("\n" + "="*60)
print("🔍 EXPERIMENTELLE KONSEQUENZEN")
print("="*60)

# Analyse der experimentellen Konsequenzen
if branching_ratios['gluons'] > 0.1:
    print("✅ STARKER GLUON-ZERFALL: In Jet-Kanälen nachweisbar")
else:
    print("❌ SCHWACHER GLUON-ZERFALL: Schwer in Jets nachweisbar")

if branching_ratios['photons'] > 0.01:
    print("✅ MESSBARER PHOTON-ZERFALL: In γγ-Kanal nachweisbar")
else:
    print("❌ SEHR SCHWACHER PHOTON-ZERFALL: Kaum in γγ nachweisbar")

if branching_ratios['quarks'] > branching_ratios['leptons']:
    print("✅ QUARK-ZERFÄLLE DOMINANT: Hauptsächlich in Hadron-Kanälen")
else:
    print("✅ LEPTON-ZERFÄLLE DOMINANT: Saubere Nachweisbarkeit")

# Plot erstellen
print("\n📊 Erstelle Visualisierung...")
coupling_calculator.plot_coupling_comparison(calculated_couplings)

print("\n💡 ZUSAMMENFASSUNG:")
print("   Basierend auf deinen 5 primordialen Parametern ergeben sich")
print("   spezifische Vorhersagen für Quark- und Gluon-Kopplungen.")
print("   Diese bestimmen die experimentelle Nachweisbarkeit!")