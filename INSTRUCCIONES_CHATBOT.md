# Instrucciones para configurar el chatbot BRAINNOVA

## Paso 1: Crear la tabla en Supabase

**Opción A: Desde el Dashboard de Supabase (Recomendado)**

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard/project/aoykpiievtadhwssugvs
2. Abre el **SQL Editor**
3. Copia y pega el contenido del archivo `scripts/setup-chatbot-db.sql`
4. Ejecuta el script (botón "Run")

**Opción B: Usando Supabase CLI**

```bash
supabase db push
```

## Paso 2: Cargar la información de BRAINNOVA

Una vez creada la tabla, ejecuta:

```bash
node scripts/process-brainnova-text.js
```

Este script procesará toda la información del PDF BRAINNOVA y la guardará en la base de datos.

## Paso 3: Verificar que los datos se guardaron

Puedes verificar en el SQL Editor de Supabase:

```sql
SELECT category, title, LEFT(content, 100) as preview 
FROM chatbot_knowledge 
ORDER BY created_at DESC;
```

Deberías ver 15 registros con información sobre:
- Sistema BRAINNOVA (objetivo, metodología)
- Las 7 dimensiones y sus subdimensiones
- Proceso de normalización y ponderación
- Información sobre encuestas
- Representación visual

## Paso 4: Probar el chatbot

Una vez cargados los datos, el chatbot podrá responder preguntas como:

- "¿Qué es BRAINNOVA?"
- "¿Cuáles son las dimensiones del sistema?"
- "¿Qué peso tiene la transformación digital empresarial?"
- "¿Cómo funciona la normalización?"
- "¿Qué información se recopila en las encuestas?"

## Notas importantes

- La tabla `chatbot_knowledge` permite lectura pública pero solo los administradores pueden insertar/actualizar datos
- Los datos se indexan automáticamente para búsquedas rápidas
- Puedes agregar más información ejecutando el script nuevamente (no duplicará datos si usas títulos únicos)

