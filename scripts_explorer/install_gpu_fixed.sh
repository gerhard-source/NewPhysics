#!/bin/bash
# Korrigiertes GPU-Installationsscript für Universum Simulator

echo "🌌 GPU-Installation für Universum Simulator"
echo "=========================================="

# System-Informationen
echo "1. System-Informationen:"
echo "   • Python: $(python3 --version 2>/dev/null || echo 'Nicht gefunden')"
echo "   • PIP: $(pip --version 2>/dev/null | head -1 || echo 'Nicht gefunden')"

# NVIDIA Check
echo ""
echo "2. Überprüfe NVIDIA Hardware..."
if command -v nvidia-smi &> /dev/null; then
    echo "   ✅ NVIDIA Treiber gefunden"
    NVIDIA_INFO=$(nvidia-smi --query-gpu=name,driver_version --format=csv,noheader | head -1)
    echo "   • GPU: $NVIDIA_INFO"
    
    # CUDA Version ermitteln
    if nvidia-smi | grep -q "CUDA Version"; then
        CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | awk '{print $9}')
        echo "   • CUDA: $CUDA_VERSION"
    else
        echo "   ❌ CUDA nicht erkannt - Installation notwendig"
        echo "   📥 Lade CUDA Toolkit von https://developer.nvidia.com/cuda-downloads"
        exit 1
    fi
else
    echo "   ❌ NVIDIA Treiber nicht gefunden"
    echo "   💡 GPU-Beschleunigung nicht verfügbar"
    echo "   🔄 Installiere nur CPU-Pakete..."
fi

# Python Pakete installieren
echo ""
echo "3. Installiere Python Pakete..."

# Grundlegende Pakete
echo "   • Installiere NumPy und Matplotlib..."
pip install numpy matplotlib

# Numba (CPU-Optimierung)
echo "   • Installiere Numba (CPU-Optimierung)..."
pip install numba

# CuPy falls NVIDIA verfügbar
if command -v nvidia-smi &> /dev/null; then
    echo "   • Installiere CuPy (GPU-Beschleunigung)..."
    
    # Bestimme CuPy Version basierend auf CUDA
    if [[ "$CUDA_VERSION" == 12.* ]]; then
        echo "   • Verwende CuPy für CUDA 12.x"
        pip install cupy-cuda12x
    elif [[ "$CUDA_VERSION" == 11.* ]]; then
        echo "   • Verwende CuPy für CUDA 11.x"
        pip install cupy-cuda11x
    else
        echo "   ⚠️  Unbekannte CUDA Version - versuche cupy-cuda11x"
        pip install cupy-cuda11x
    fi
else
    echo "   💡 Überspringe CuPy (keine NVIDIA GPU)"
fi

echo ""
echo "✅ Installation abgeschlossen!"
echo ""
echo "🚀 Starte den Simulator: python3 UniversumSimulator_gpu.py"
echo ""
echo "📊 Verfügbare Modi:"
echo "   • CPU-Modus: ~100-500 Körper/Sekunde"
echo "   • GPU-Modus: ~1.000-5.000 Körper/Sekunde (falls verfügbar)"
