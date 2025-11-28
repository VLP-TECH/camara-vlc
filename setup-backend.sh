#!/bin/bash

# Script para copiar el backend al repositorio del frontend
# El backend se copia directamente en la raíz del repositorio
# Uso: ./setup-backend.sh /ruta/al/backend

set -e

BACKEND_SOURCE="${1:-}"

if [ -z "$BACKEND_SOURCE" ]; then
    echo "❌ Error: Debes proporcionar la ruta al directorio del backend"
    echo ""
    echo "Uso: ./setup-backend.sh /ruta/al/backend"
    echo ""
    echo "Ejemplo:"
    echo "  ./setup-backend.sh ~/Downloads/Camara_de_comercio"
    exit 1
fi

if [ ! -d "$BACKEND_SOURCE" ]; then
    echo "❌ Error: El directorio '$BACKEND_SOURCE' no existe"
    exit 1
fi

echo "📦 Copiando backend desde: $BACKEND_SOURCE"
echo "   → Copiando directamente en la raíz del repositorio"
echo ""

# Archivos y directorios esenciales a copiar
ESSENTIAL_FILES=(
    "main.py"
    "requirements.txt"
    "microservicio_exposicion"
    "microservicio_ingesta"
    "database"
    "config"
    "modelos"
)

# Copiar archivos esenciales a la raíz
for item in "${ESSENTIAL_FILES[@]}"; do
    if [ -e "$BACKEND_SOURCE/$item" ]; then
        echo "  ✓ Copiando $item..."
        # Si ya existe, preguntar o sobrescribir
        if [ -e "$item" ]; then
            echo "    ⚠ $item ya existe, sobrescribiendo..."
        fi
        cp -r "$BACKEND_SOURCE/$item" .
    else
        echo "  ⚠ No se encontró: $item"
    fi
done

# Verificar que requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo ""
    echo "❌ Error: No se encontró requirements.txt en el backend"
    exit 1
fi

# Verificar que main.py existe
if [ ! -f "main.py" ]; then
    echo ""
    echo "❌ Error: No se encontró main.py en el backend"
    exit 1
fi

echo ""
echo "✅ Backend copiado correctamente en la raíz del repositorio"
echo ""
echo "📋 Próximos pasos:"
echo "  1. Revisa que requirements.txt esté completo"
echo "  2. Copia env.example a .env y configura las variables"
echo "  3. Ejecuta: docker-compose up -d"
echo ""

