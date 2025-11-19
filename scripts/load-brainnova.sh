#!/bin/bash

echo "🔍 Verificando si la tabla chatbot_knowledge existe..."
echo ""

# Intentar cargar los datos
node scripts/process-brainnova-text.js

# Verificar el resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Datos cargados exitosamente!"
    echo ""
    echo "El chatbot ahora puede responder preguntas sobre:"
    echo "  • Las 7 dimensiones del sistema BRAINNOVA"
    echo "  • Proceso de normalización y ponderación"
    echo "  • Información sobre encuestas"
    echo "  • Metodología del sistema"
else
    echo ""
    echo "❌ La tabla aún no existe."
    echo ""
    echo "Por favor ejecuta el SQL en Supabase:"
    echo "  https://supabase.com/dashboard/project/aoykpiievtadhwssugvs/sql/new"
    echo ""
    echo "Copia el contenido de: scripts/setup-chatbot-db.sql"
    echo ""
    echo "Luego ejecuta este script nuevamente:"
    echo "  npm run load-brainnova"
fi

