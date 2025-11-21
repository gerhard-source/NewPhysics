#!/bin/bash
# GPU-Installationsscript für Universum Simulator

echo "🌌 GPU-Installation für Universum Simulator"
echo "=========================================="

# NVIDIA Treiber überprüfen
echo "1. Überprüfe NVIDIA Treiber..."
if command -v nvidia-smi &> /dev/null; then
    echo "   ✅ NVIDIA Treiber gefunden"
    nvidia-smi --query-gpu=driver_version --format=csv,noheader
else
    echo "   ❌ NVIDIA Treiber nicht gefunden"
    echo "   Bitte installieren Sie zuerst die NVIDIA Treiber"
    exit 1
fi

# CUDA Version ermitteln
echo "2. Ermittle CUDA Version..."
CUDA_VERSION=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | cut -d'.' -f1)
if [ "$CUDA_VERSION" -ge 12 ]; then
    echo "   ✅ CUDA 12.x kompatible GPU gefunden"
    PIP_PACKAGE="cupy-cuda12x"
elif [ "$CUDA_VERSION" -ge 11 ]; then
    echo "   ✅ CUDA 11.x kompatible GPU gefunden" 
    PIP_PACKAGE="cupy-cuda11x"
else
    echo "   ❌ Keine kompatible CUDA Version gefunden"
    exit 1
fi

# Bibliotheken installieren
echo "3. Installiere CuPy ($PIP_PACKAGE)..."
pip install $PIP_PACKAGE

echo "4. Installiere Numba..."
pip install numba

echo ""
echo "✅ Installation abgeschlossen!"
echo "🚀 Starten Sie den Simulator neu: python3 UniversumSimulator_gpu.py"
