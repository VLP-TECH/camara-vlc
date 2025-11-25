# Cargar datos de Brainnova en Supabase

Este script carga los datos del backend de Brainnova (dimensiones, subdimensiones, indicadores y componentes) en Supabase.

## Requisitos

1. **Python 3.8+** con las dependencias del backend instaladas
2. **Clave de servicio de Supabase** (Service Role Key)
3. **Acceso al directorio del backend** con los datos procesados

## Configuración

1. Obtén la Service Role Key de Supabase:
   - Ve a: https://supabase.com/dashboard/project/aoykpiievtadhwssugvs/settings/api
   - Copia la "service_role" key (⚠️ **NUNCA** la compartas públicamente)

2. Configura la variable de entorno:
   ```bash
   export VITE_SUPABASE_SERVICE_ROLE_KEY="tu-service-role-key-aqui"
   ```

   O crea un archivo `.env` en el directorio del script:
   ```
   VITE_SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key-aqui
   ```

## Ejecución

### Opción 1: Desde el directorio del backend

```bash
cd /Users/chaumesanchez/Downloads/Camara_de_comercio
python ../camara-vlc/scripts/load-brainnova-to-supabase.py
```

### Opción 2: Desde el directorio del frontend

```bash
cd /Users/chaumesanchez/Documents/camara-vlc
python scripts/load-brainnova-to-supabase.py
```

## Qué carga el script

1. **Dimensiones**: Las 7 dimensiones del sistema Brainnova
2. **Subdimensiones**: Todas las subdimensiones asociadas a cada dimensión
3. **Indicadores**: Todos los indicadores definidos en el catálogo
4. **Componentes**: Los componentes de datos asociados a cada indicador

## Notas importantes

- El script usa `upsert` para evitar duplicados (actualiza si existe, inserta si no)
- Los datos crudos y macro deben cargarse por separado desde los CSV procesados
- Asegúrate de que las tablas existan en Supabase antes de ejecutar (ejecuta la migración primero)

## Solución de problemas

### Error: "No module named 'supabase'"
```bash
pip install supabase
```

### Error: "No se pueden importar módulos del backend"
- Asegúrate de ejecutar el script desde el directorio correcto
- Verifica que el path al backend sea correcto en el script

### Error: "Service Role Key no configurada"
- Verifica que la variable de entorno esté configurada
- Asegúrate de usar la Service Role Key, no la anon key

