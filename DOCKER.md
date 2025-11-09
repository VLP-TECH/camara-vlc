# 🐳 Guía de Dockerización - Ecosistema Valencia View

## 📋 Requisitos Previos

- Docker instalado (versión 20.10 o superior)
- Docker Compose instalado (versión 2.0 o superior)

## 🚀 Construcción y Ejecución

### Opción 1: Usando Docker Compose (Recomendado)

```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reconstruir después de cambios
docker-compose up -d --build
```

### Opción 2: Usando Docker directamente

```bash
# Construir la imagen
docker build -t ecosistema-valencia-view .

# Ejecutar el contenedor
docker run -d \
  --name ecosistema-valencia-view \
  -p 4173:4173 \
  -e NODE_ENV=production \
  -e PORT=4173 \
  --restart unless-stopped \
  ecosistema-valencia-view

# Ver logs
docker logs -f ecosistema-valencia-view

# Detener
docker stop ecosistema-valencia-view

# Eliminar
docker rm ecosistema-valencia-view
```

## 🔧 Variables de Entorno

Puedes pasar variables de entorno al contenedor:

```bash
# Con Docker Compose (editar docker-compose.yml)
environment:
  - NODE_ENV=production
  - PORT=4173
  - VITE_SUPABASE_URL=tu-url
  - VITE_SUPABASE_ANON_KEY=tu-key

# Con Docker directamente
docker run -d \
  -e VITE_SUPABASE_URL=tu-url \
  -e VITE_SUPABASE_ANON_KEY=tu-key \
  ecosistema-valencia-view
```

## 📦 Estructura del Dockerfile

El Dockerfile usa multi-stage build para optimizar el tamaño:

1. **Builder stage**: Construye la aplicación
2. **Runner stage**: Solo incluye archivos necesarios para producción

## 🔍 Comandos Útiles

```bash
# Ver imágenes
docker images | grep ecosistema-valencia-view

# Ver contenedores
docker ps -a | grep ecosistema-valencia-view

# Entrar al contenedor
docker exec -it ecosistema-valencia-view sh

# Ver uso de recursos
docker stats ecosistema-valencia-view

# Limpiar imágenes no usadas
docker image prune -a
```

## 🐛 Troubleshooting

### Error: "Cannot find module"
```bash
# Reconstruir sin cache
docker-compose build --no-cache
```

### Error: "Port already in use"
```bash
# Cambiar el puerto en docker-compose.yml
ports:
  - "4174:4173"  # Puerto externo:puerto interno
```

### Ver logs de errores
```bash
docker-compose logs app
# o
docker logs ecosistema-valencia-view
```

### Reconstruir después de cambios
```bash
docker-compose up -d --build
```

## 🚀 Despliegue en Producción

### Con Docker Compose

```bash
# 1. Clonar repositorio
git clone https://github.com/VLP-TECH/ecosistema-valencia-view.git
cd ecosistema-valencia-view

# 2. Configurar variables de entorno (opcional)
# Editar docker-compose.yml o crear .env

# 3. Construir y ejecutar
docker-compose up -d --build

# 4. Verificar que está corriendo
docker-compose ps
curl http://localhost:4173
```

### Con Docker directamente

```bash
# 1. Construir
docker build -t ecosistema-valencia-view:latest .

# 2. Ejecutar
docker run -d \
  --name ecosistema-valencia-view \
  -p 4173:4173 \
  --restart unless-stopped \
  ecosistema-valencia-view:latest
```

## 🔒 Seguridad

- El contenedor corre con un usuario no-root (nextjs)
- Solo se copian archivos necesarios para producción
- Health check configurado para monitoreo

## 📊 Monitoreo

El contenedor incluye un health check que verifica cada 30 segundos:

```bash
# Ver estado del health check
docker inspect --format='{{.State.Health.Status}}' ecosistema-valencia-view
```

## 🔄 Actualización

```bash
# 1. Obtener últimos cambios
git pull

# 2. Reconstruir y reiniciar
docker-compose up -d --build

# O con Docker directamente
docker build -t ecosistema-valencia-view:latest .
docker stop ecosistema-valencia-view
docker rm ecosistema-valencia-view
docker run -d --name ecosistema-valencia-view -p 4173:4173 ecosistema-valencia-view:latest
```


