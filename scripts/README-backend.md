# 🚀 Guía para Arrancar el Backend de Brainnova

El backend de Brainnova es una API FastAPI que proporciona los datos para el frontend.

## 📋 Requisitos Previos

1. **Python 3.8+** instalado
2. **PostgreSQL** (o usar Docker que lo incluye)
3. **Dependencias de Python** instaladas

## 🎯 Opción 1: Arrancar con Docker (Recomendado)

Esta opción es la más sencilla porque incluye la base de datos PostgreSQL.

### Pasos:

1. **Asegúrate de tener Docker instalado:**
   ```bash
   docker --version
   ```

2. **Arranca el backend:**
   ```bash
   cd /Users/chaumesanchez/Downloads/Camara_de_comercio
   docker-compose up --build
   ```
   
   O usa el script:
   ```bash
   bash scripts/start-backend-docker.sh
   ```

3. **El backend estará disponible en:**
   - API: http://127.0.0.1:8000
   - Base de datos: localhost:5432
   - Documentación API: http://127.0.0.1:8000/docs

### Detener el backend:
```bash
docker-compose down
```

## 🐍 Opción 2: Arrancar con Python Directamente

Si prefieres no usar Docker, puedes arrancar el backend directamente.

### Pasos:

1. **Navega al directorio del backend:**
   ```bash
   cd /Users/chaumesanchez/Downloads/Camara_de_comercio
   ```

2. **Crea y activa un entorno virtual (recomendado):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En macOS/Linux
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**
   - Asegúrate de tener PostgreSQL corriendo
   - Configura las credenciales en `database/config.py` o variables de entorno

5. **Arranca el servidor:**
   ```bash
   python3 main.py
   ```
   
   O usa el script:
   ```bash
   bash scripts/start-backend.sh
   ```

6. **El backend estará disponible en:**
   - API: http://127.0.0.1:8000
   - Documentación API: http://127.0.0.1:8000/docs

## 🔧 Configuración de Base de Datos

El backend necesita una base de datos PostgreSQL. Tienes dos opciones:

### Opción A: Usar Docker (automático)
Si usas `docker-compose`, la base de datos se crea automáticamente.

### Opción B: Base de datos local
1. Instala PostgreSQL
2. Crea una base de datos llamada `indicadores`
3. Configura las credenciales en `database/config.py`:
   ```python
   DB_HOST = "localhost"
   DB_PORT = 5432
   DB_USER = "postgres"
   DB_PASSWORD = "tu_password"
   DB_NAME = "indicadores"
   ```

## 📝 Endpoints Disponibles

Una vez arrancado, el backend expone estos endpoints:

- `GET /api/v1/indicadores-disponibles` - Lista de indicadores
- `GET /api/v1/filtros-globales` - Filtros disponibles
- `GET /api/v1/resultados` - Resultados históricos
- `POST /api/v1/brainnova-score` - Calcular Brainnova Score
- `GET /docs` - Documentación interactiva (Swagger)

## 🐛 Solución de Problemas

### Error: "No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### Error: "Connection refused" a la base de datos
- Verifica que PostgreSQL esté corriendo
- Verifica las credenciales en `database/config.py`
- Si usas Docker, asegúrate de que el contenedor de la BD esté corriendo

### Error: "Port 8000 already in use"
```bash
# Encontrar proceso usando el puerto
lsof -i :8000

# Matar el proceso
kill -9 <PID>
```

### El backend arranca pero no hay datos
- Asegúrate de que la base de datos tenga datos
- Verifica que las tablas existan
- Revisa los logs del backend para errores

## 📚 Documentación Adicional

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## ✅ Verificación

Para verificar que el backend está funcionando:

```bash
curl http://127.0.0.1:8000/api/v1/indicadores-disponibles
```

Deberías recibir una lista JSON de indicadores.

