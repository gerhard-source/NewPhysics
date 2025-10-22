#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution

class AdvancedConstantReconstructor:
    """Verbesserte Version mit physikalisch realistischen Transformationen"""
    
    def __init__(self):
        self.observed_constants = {
            'fine_structure': 1/137.035999,
            'proton_electron_ratio': 1836.15,
            'cosmological_constant': 1.0e-122,
            'baryon_ratio': 0.048,
            'weak_angle': 0.2223,  # Sin²(θ_W) - Weinberg-Winkel
        }
        
    def physics_based_transformation(self, fundamental_params):
        """Physikalisch motivierte Transformationen"""
        # fundamental_params = [Urenergie, Urkopplung, Ursymmetrie]
        E, g, S = fundamental_params
        
        simulated = {}
        
        # Feinstrukturkonstante: Quantenelektrodynamik-artig
        # α = g²/4π mit Renormierungs-Effekten
        simulated['fine_structure'] = (g**2 / (4 * np.pi)) * (1 + 0.1 * np.sin(E))
        
        # Massenverhältnis: Higgs-Mechanismus-artig
        # m_p/m_e ~ Yukawa-Kopplungen + Symmetriebrechung
        simulated['proton_electron_ratio'] = 1800 + 200 * np.tanh(S * g)
        
        # Kosmologische Konstante: Vakuumenergie
        # Λ ~ exp(-S) * Quantenfluktuationen
        simulated['cosmological_constant'] = np.exp(-E**2 - S**2) * 1e-122
        
        # Baryon-Asymmetrie: CP-Verletzung + sphaleron-Übergänge
        simulated['baryon_ratio'] = 0.05 * (1 + 0.2 * np.sin(g * S))
        
        # Schwacher Weinberg-Winkel: SU(2)×U(1) Symmetriebrechung
        simulated['weak_angle'] = 0.23 + 0.02 * np.tanh(E - g)
        
        return simulated
    
    def enhanced_fitness(self, fundamental_params):
        """Verbesserte Fehlerfunktion mit physikalischen Gewichten"""
        simulated = self.physics_based_transformation(fundamental_params)
        
        # Physikalisch sinnvolle Gewichtung
        weights = {
            'fine_structure': 1.0,
            'proton_electron_ratio': 0.8, 
            'cosmological_constant': 0.3,  # Weniger Gewicht wegen Messunsicherheit
            'baryon_ratio': 0.7,
            'weak_angle': 0.9
        }
        
        error = 0.0
        for key in self.observed_constants:
            obs = self.observed_constants[key]
            sim = simulated[key]
            weight = weights[key]
            
            # Logarithmischer Fehler für große Dynamikbereiche
            if key == 'cosmological_constant':
                log_error = (np.log10(obs) - np.log10(sim))**2
                error += weight * log_error
            else:
                rel_error = ((sim - obs) / obs)**2
                error += weight * rel_error
                
        return error
    
    def robust_optimization(self):
        """Robustere Optimierung mit evolutionärem Algorithmus"""
        print("🔍 Starte erweiterte Suche nach Ur-Konstanten...")
        
        # Grenzen für fundamentale Parameter
        bounds = [(-5, 5), (-5, 5), (-5, 5)]  # E, g, S
        
        # Evolutionärer Algorithmus für globale Optimierung
        result = differential_evolution(self.enhanced_fitness, bounds, 
                                      strategy='best1bin', maxiter=1000, 
                                      popsize=15, tol=1e-6)
        
        self.fundamental_params = result.x
        print(f"✅ Optimale fundamentale Parameter: {self.fundamental_params}")
        print(f"🏁 Finaler Fehler: {result.fun:.6f}")
        
        return self.fundamental_params
    
    def analyze_sensitivity(self):
        """Analysiert wie sensitiv jede Konstante auf Ur-Parameter reagiert"""
        print("\n🎯 Sensitivitätsanalyse:")
        
        base_params = self.fundamental_params
        base_constants = self.physics_based_transformation(base_params)
        
        perturbations = [0.1, 0.01, 0.001]
        
        for i, param_name in enumerate(['Energie', 'Kopplung', 'Symmetrie']):
            print(f"\n--- Sensitivität auf {param_name} ---")
            
            for pert in perturbations:
                # Perturbiere einen Parameter
                test_params = base_params.copy()
                test_params[i] += pert
                
                test_constants = self.physics_based_transformation(test_params)
                
                print(f"  Δ{param_name} = {pert}:")
                for key in ['fine_structure', 'proton_electron_ratio']:
                    change = abs((test_constants[key] - base_constants[key]) / base_constants[key]) * 100
                    print(f"    {key}: {change:.2f}% Änderung")

# Test der verbesserten Version
if __name__ == "__main__":
    print("=" * 70)
    print("🔬 VERBESSERTE KONSTANTEN-ABLEITUNG - Physikalische Transformationen")
    print("=" * 70)
    
    advanced = AdvancedConstantReconstructor()
    best_params = advanced.robust_optimization()
    
    # Zeige finale Ergebnisse
    final_constants = advanced.physics_based_transformation(best_params)
    print("\n" + "="*50)
    print("FINALER VERGLEICH:")
    print("="*50)
    
    for key in advanced.observed_constants:
        obs = advanced.observed_constants[key]
        sim = final_constants[key]
        error_pct = abs((sim - obs) / obs) * 100
        status = "✅" if error_pct < 10 else "⚠️" if error_pct < 30 else "❌"
        
        print(f"{status} {key:25}: {obs:12.6e} → {sim:12.6e} | Fehler: {error_pct:6.2f}%")
    
    # Sensitivitätsanalyse
    advanced.analyze_sensitivity()

