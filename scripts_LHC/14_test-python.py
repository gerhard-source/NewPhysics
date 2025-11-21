#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")

try:
    import numpy
    print("✓ numpy verfügbar")
except ImportError:
    print("✗ numpy nicht verfügbar")

try:
    import matplotlib
    print("✓ matplotlib verfügbar") 
except ImportError:
    print("✗ matplotlib nicht verfügbar")

try:
    import scipy
    print("✓ scipy verfügbar")
except ImportError:
    print("✗ scipy nicht verfügbar")

