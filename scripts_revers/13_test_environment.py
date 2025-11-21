#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# /home/gh/Schreibtisch/physik/py/scripts/13_test_environment.py


Created on Tue Nov  4 12:49:30 2025

@author: gh
"""
import sys
import uproot
import numpy as np
import matplotlib.pyplot as plt

print("✅ Virtual Environment aktiviert!")
print("📁 Arbeitsverzeichnis:", sys.path[0])
print("🐍 Python-Pfad:", sys.executable)

# Test-Plot erstellen
plt.figure(figsize=(10, 6))
masses = np.linspace(800, 1200, 100)
signal = np.exp(-0.5*((masses - 1000)/50)**2)  # Signal bei 1 TeV
plt.plot(masses, signal, 'r-', linewidth=2, label='Skalares Teilchen ~1 TeV')
plt.xlabel('Invariante Masse [GeV]')
plt.ylabel('Signalisärke')
plt.title('Vorhersage deines Modells')
plt.legend()
plt.grid(True)
plt.savefig('./results/test_plot.png')
plt.show()

print("✅ Plot gespeichert in /results/")