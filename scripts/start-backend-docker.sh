#!/bin/bash
# Script para arrancar el backend con Docker

BACKEND_DIR="/Users/chaumesanchez/Downloads/Camara_de_comercio"

echo "🐳 Iniciando backend de Brainnova con Docker..."
echo ""

# Verificar que el directorio existe
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Error: No se encuentra el directorio del backend: $BACKEND_DIR"
    exit 1
fi

cd "$BACKEND_DIR"

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    echo "   Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Verificar si docker-compose está disponible
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Error: docker-compose no está disponible"
    exit 1
fi

echo "📦 Construyendo y arrancando contenedores..."
echo ""

$COMPOSE_CMD up --build

echo ""
echo "✅ Backend disponible en: http://127.0.0.1:8000"
echo "   Base de datos PostgreSQL en: localhost:5432"
echo ""
echo "   Para detener: Ctrl+C o 'docker-compose down'"

