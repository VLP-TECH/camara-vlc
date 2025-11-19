# Configuración del Chatbot con Base de Datos

Este documento explica cómo configurar el chatbot para que responda preguntas sobre encuestas y KPIs usando información extraída de PDFs.

## Estructura

1. **Base de datos**: Tabla `chatbot_knowledge` en Supabase para almacenar información
2. **Script de procesamiento**: `scripts/process-pdf-knowledge.js` para extraer información de PDFs
3. **Servicio**: `src/lib/chatbot-service.ts` para consultar la base de datos
4. **Componente**: `src/components/ChatWidget.tsx` actualizado para usar el servicio

## Pasos para configurar

### 1. Ejecutar la migración de base de datos

La migración ya está creada en `supabase/migrations/20250102000000_create_chatbot_knowledge.sql`. 

Si usas Supabase CLI:
```bash
supabase db push
```

O ejecuta la migración manualmente desde el dashboard de Supabase.

### 2. Instalar dependencias para procesar PDFs

```bash
npm install pdf-parse
```

### 3. Procesar el PDF

Una vez que tengas el PDF con la información:

```bash
node scripts/process-pdf-knowledge.js ruta/al/archivo.pdf
```

El script:
- Extrae el texto del PDF
- Identifica secciones (KPIs, encuestas, información general)
- Extrae palabras clave
- Guarda todo en la tabla `chatbot_knowledge`

### 4. Verificar los datos

Puedes verificar que los datos se guardaron correctamente desde el dashboard de Supabase o ejecutando:

```sql
SELECT * FROM chatbot_knowledge ORDER BY created_at DESC;
```

## Cómo funciona

### Búsqueda de información

El chatbot busca información en la base de datos usando:
- Búsqueda por texto completo en títulos y contenido
- Coincidencia de palabras clave
- Categorización (survey, kpi, general)

### Respuestas inteligentes

El chatbot puede responder sobre:
- **Encuestas**: Lista encuestas disponibles y sus detalles
- **KPIs**: Proporciona información sobre indicadores y métricas
- **Información general**: Responde basándose en el contenido del PDF

### Ejemplo de uso

Usuario: "¿Qué encuestas hay disponibles?"
Chatbot: Consulta la tabla `surveys` y lista las encuestas activas.

Usuario: "¿Cuáles son los KPIs principales?"
Chatbot: Busca en `chatbot_knowledge` con categoría 'kpi' y devuelve la información relevante.

## Personalización

### Agregar más categorías

Puedes agregar más categorías editando el script `process-pdf-knowledge.js` y agregando patrones de reconocimiento.

### Mejorar las búsquedas

Edita `src/lib/chatbot-service.ts` para ajustar:
- El algoritmo de relevancia
- El número de resultados
- Los filtros de búsqueda

## Notas

- El chatbot requiere que el usuario esté autenticado para consultar algunas tablas (según las políticas RLS)
- La búsqueda usa PostgreSQL full-text search en español
- Los keywords se extraen automáticamente del contenido

