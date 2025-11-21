#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ~/physik/scripts/31_create_paper_figures.py   fehlerhaft

Created on Tue Nov  4 18:40:47 2025

@author: gh
"""

import matplotlib.pyplot as plt
import numpy as np

def create_all_figures():
    """Erstellt alle benötigten Paper-Figuren"""

    # 1. Discovery Timeline
    fig1 = create_discovery_timeline()

    # 2. Coupling Comparison
    fig2 = create_coupling_comparison()

    # 3. Branching Ratio Chart
    fig3 = create_branching_ratios()

    # 4. Significance Projection
    fig4 = create_significance_projection()

create_all_figures()
