#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/physik/scripts/parameter_optimization.py
import numpy as np
import matplotlib.pyplot as plt

class ParameterOptimization:
    def __init__(self):
        self.original_params = {
            'mass': 1000.0, 'width': 25.0,
            'coupling_e': 0.001, 'coupling_mu': 0.001, 'coupling_tau': 0.0005
        }
    
    def find_experimental_limits(self):
        """Vergleicht mit experimentellen Ausschlussgrenzen"""
        # Typische aktuelle Limits für skalare Teilchen bei 1 TeV:
        current_limits = {
            'coupling_upper_limit': 0.0003,  # Konservativer Wert
            'excluded_mass_ranges': [(900, 1100)],  # Beispiel
        }
        return current_limits
    
    def optimize_parameters(self):
        """Findet Parameter, die mit Experimenten kompatibel sind"""
        limits = self.find_experimental_limits()
        
        # Angepasste Parameter
        optimized = self.original_params.copy()
        optimized['coupling_e'] = limits['coupling_upper_limit'] * 0.8  # Sicherheitsabstand
        optimized['coupling_mu'] = limits['coupling_upper_limit'] * 0.8
        optimized['coupling_tau'] = limits['coupling_upper_limit'] * 0.6
        
        return optimized

# Teste angepasste Parameter
optimizer = ParameterOptimization()
optimized_params = optimizer.optimize_parameters()

print("🔬 Parameter-Optimierung:")
print(f"Original: coupling_e = {optimizer.original_params['coupling_e']}")
print(f"Optimiert: coupling_e = {optimized_params['coupling_e']}")
print(f"Reduktion um: {(1-optimized_params['coupling_e']/optimizer.original_params['coupling_e'])*100:.1f}%")