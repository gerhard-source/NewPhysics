# -*- coding: utf-8 -*-
# ~/physik/scripts/scalar_analysis.py
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Pfade für deine Struktur
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ReverseReconstructionAnalysis:
    def __init__(self):
        # DEINE Vorhersagen aus der Rückwärtssimulation hier eintragen!
        self.scalar_mass = 1000.0      # Masse in GeV - ANPASSEN!
        self.scalar_width = 25.0       # Breite in GeV - ANPASSEN!
        self.coupling_e = 0.001        # Kopplung an Elektronen - ANPASSEN!
        self.coupling_mu = 0.001       # Kopplung an Myonen - ANPASSEN!
        
    def get_predictions_from_your_model(self):
        """Hier kommen die exakten Werte aus DEINER 5-Parameter-Berechnung"""
        # Beispiel - mit deinen echten Werten ersetzen!
        predictions = {
            'mass': 1000.0,      # GeV
            'width': 25.0,       # GeV  
            'coupling_e': 0.001,
            'coupling_mu': 0.001,
            'coupling_tau': 0.0005,
            'branching_ratio_ee': 0.4,
            'branching_ratio_mumu': 0.4,
            'branching_ratio_tautau': 0.2
        }
        return predictions
    
    def simulate_lhc_signature(self):
        """Simuliert das erwartete Signal am LHC"""
        pred = self.get_predictions_from_your_model()
        
        # Energiebereich für die Suche
        energy = np.linspace(800, 1200, 200)
        
        # Breit-Wigner-artige Resonanz
        signal = (pred['coupling_e']**2 * 
                 (pred['width']**2 / 
                  ((energy - pred['mass'])**2 + (pred['width']/2)**2)))
        
        return energy, signal, pred
    
    def plot_analysis(self):
        """Erstellt die Analyse-Plots"""
        energy, signal, predictions = self.simulate_lhc_signature()
        
        # Plot erstellen
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Signalplot
        ax1.plot(energy, signal, 'r-', linewidth=3, 
                label=f'Skalar {predictions["mass"]} GeV')
        ax1.set_xlabel('Invariante Masse [GeV]')
        ax1.set_ylabel('Signalisärke')
        ax1.set_title('Vorhersage: Skalares Kraftvermittlungsteilchen')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Kopplungsstärken
        couplings = ['e', 'μ', 'τ']
        values = [predictions['coupling_e'], predictions['coupling_mu'], 
                 predictions.get('coupling_tau', 0.0005)]
        
        ax2.bar(couplings, values, color=['blue', 'green', 'red'])
        ax2.set_ylabel('Kopplungsstärke')
        ax2.set_title('Kopplungen an Leptonen')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../results/scalar_predictions.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return predictions

# Hauptprogramm
if __name__ == "__main__":
    print("🚀 Starte Reverse-Reconstruction Analyse")
    print("📁 Arbeitsverzeichnis: ~/physik/")
    
    analysis = ReverseReconstructionAnalysis()
    predictions = analysis.plot_analysis()
    
    print("\n📊 Vorhersagen deines Modells:")
    for key, value in predictions.items():
        print(f"   {key}: {value}")
    
    print(f"\n💡 Nächster Schritt: Öffne Spyder und passe die Werte an DEINE Berechnungen an!")