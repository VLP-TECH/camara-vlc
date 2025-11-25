#!/bin/bash
# Script para arrancar el backend de Brainnova

BACKEND_DIR="/Users/chaumesanchez/Downloads/Camara_de_comercio"

echo "🚀 Iniciando backend de Brainnova..."
echo ""

# Verificar que el directorio existe
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Error: No se encuentra el directorio del backend: $BACKEND_DIR"
    exit 1
fi

cd "$BACKEND_DIR"

# Verificar si hay un entorno virtual
if [ -d "venv" ] || [ -d ".venv" ]; then
    echo "📦 Activando entorno virtual..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        source .venv/bin/activate
    fi
fi

# Verificar si hay conda
if command -v conda &> /dev/null; then
    echo "📦 Verificando entorno conda..."
    if conda env list | grep -q "camara_env"; then
        echo "   Activando entorno conda: camara_env"
        conda activate camara_env
    fi
fi

# Verificar dependencias
echo "🔍 Verificando dependencias..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "⚠️  FastAPI no está instalado"
    echo "   Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
fi

# Verificar base de datos
echo "🔍 Verificando configuración de base de datos..."
if [ -f "database/config.py" ]; then
    echo "   ✅ Configuración encontrada"
else
    echo "   ⚠️  Configuración no encontrada"
fi

# Arrancar el servidor
echo ""
echo "🌐 Arrancando servidor en http://127.0.0.1:8000"
echo "   Presiona Ctrl+C para detener el servidor"
echo ""

python3 main.py

