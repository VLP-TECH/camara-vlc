# Cámara de Comercio de Valencia - Plataforma Digital

Plataforma integral para el análisis, monitorización y desarrollo del ecosistema digital valenciano.

## Descripción

Esta aplicación proporciona una plataforma completa para:
- Análisis de indicadores económicos y KPIs
- Visualización de datos abiertos
- Gestión de encuestas y participación ciudadana
- Dashboard administrativo para gestión de usuarios
- Gráficos de tendencias e indicadores
- Cálculo del Brainnova Score

## Tecnologías

Este proyecto está construido con:

- **Vite** - Build tool y dev server
- **TypeScript** - Lenguaje de programación
- **React** - Biblioteca de UI
- **shadcn-ui** - Componentes de UI
- **Tailwind CSS** - Framework de estilos
- **Supabase** - Backend y autenticación
- **Recharts** - Visualización de datos
- **React Query** - Gestión de estado del servidor

## Instalación

### Requisitos previos

- Node.js (versión 18 o superior) - [Instalar con nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
- npm o yarn
- Cuenta de Supabase configurada
- (Opcional) Backend de Brainnova para funcionalidades avanzadas

### Pasos de instalación

```sh
# Paso 1: Clonar el repositorio
git clone <YOUR_GIT_URL>

# Paso 2: Navegar al directorio del proyecto
cd camara-vlc

# Paso 3: Instalar las dependencias
npm install

# Paso 4: Configurar variables de entorno
# Crear archivo .env en la raíz del proyecto con:
VITE_SUPABASE_URL=tu-url-de-supabase
VITE_SUPABASE_ANON_KEY=tu-clave-anon-de-supabase
VITE_API_BASE_URL=http://127.0.0.1:8000  # Opcional: URL del backend de Brainnova

# Paso 5: Ejecutar migraciones de Supabase (si es necesario)
# Las migraciones se encuentran en supabase/migrations/

# Paso 6: Iniciar el servidor de desarrollo
npm run dev
```

## Scripts disponibles

- `npm run dev` - Inicia el servidor de desarrollo (puerto 8080)
- `npm run build` - Construye la aplicación para producción
- `npm run start` - Inicia el servidor de preview de producción (puerto 4173)

## Estructura del proyecto

```
camara-vlc/
├── src/
│   ├── components/     # Componentes React reutilizables
│   ├── pages/          # Páginas de la aplicación
│   ├── hooks/          # Custom hooks
│   ├── contexts/       # Context providers
│   ├── integrations/  # Integraciones con servicios externos
│   └── lib/            # Utilidades y helpers
├── public/             # Archivos estáticos
├── supabase/          # Configuración y migraciones de Supabase
├── scripts/           # Scripts de utilidad y carga de datos
└── ...
```

## 🚀 Despliegue a Producción

### Prerrequisitos para Producción

1. **Variables de Entorno Requeridas:**
   ```bash
   VITE_SUPABASE_URL=https://tu-proyecto.supabase.co
   VITE_SUPABASE_ANON_KEY=tu-clave-publica-de-supabase
   VITE_API_BASE_URL=https://tu-backend.com  # Opcional
   NODE_ENV=production
   PORT=4173  # Puerto para el servidor de preview
   ```

2. **Base de Datos Supabase:**
   - Asegúrate de que todas las migraciones estén aplicadas
   - Verifica que las políticas RLS estén configuradas correctamente
   - Confirma que los datos necesarios estén cargados

3. **Backend de Brainnova (Opcional):**
   - Si usas funcionalidades de Brainnova Score o Tendencias, asegúrate de que el backend esté disponible
   - La aplicación tiene fallback a Supabase si el backend no está disponible

### Opción 1: Despliegue con Docker Compose (Recomendado)

Este método despliega frontend, backend y PostgreSQL en un solo comando.

#### Preparación

1. **Copiar el backend al repositorio (en la raíz):**

   **Opción A: Usar el script automatizado (Recomendado):**
   ```bash
   # Ejecutar el script de setup
   ./setup-backend.sh /ruta/al/backend
   
   # Ejemplo:
   ./setup-backend.sh ~/Downloads/Camara_de_comercio
   ```
   
   El script copiará los archivos del backend directamente en la raíz del repositorio:
   - `main.py`
   - `requirements.txt`
   - `microservicio_exposicion/`
   - `database/`
   - `config/`

   **Opción B: Copiar manualmente:**
   ```bash
   # Copiar archivos esenciales directamente en la raíz
   cp /ruta/al/backend/main.py .
   cp /ruta/al/backend/requirements.txt .
   cp -r /ruta/al/backend/microservicio_exposicion .
   cp -r /ruta/al/backend/database .
   cp -r /ruta/al/backend/config .
   ```

2. **Configurar variables de entorno:**
   ```bash
   # Copiar el archivo de ejemplo
   cp env.example .env
   
   # Editar .env con tus valores reales
   nano .env
   ```

3. **Variables de entorno necesarias (.env):**
   ```bash
   # Base de datos
   DB_USER=postgres
   DB_PASSWORD=tu_password_seguro
   DB_NAME=indicadores
   DB_PORT=5432
   
   # Backend
   BACKEND_PORT=8000
   
   # Frontend
   PORT=4173
   NODE_ENV=production
   VITE_SUPABASE_URL=https://tu-proyecto.supabase.co
   VITE_SUPABASE_ANON_KEY=tu-clave-anon
   ```

#### Despliegue

```bash
# Construir y levantar todos los servicios
docker-compose up -d

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f db

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (¡cuidado! esto borra la BD)
docker-compose down -v
```

#### Servicios disponibles

- **Frontend:** http://localhost:4173
- **Backend API:** http://localhost:8000
- **Backend Docs:** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432

### Opción 2: Despliegue en EasyPanel con Docker Compose

1. **Configuración del Repositorio:**
   - URL: `https://github.com/tu-usuario/camara-vlc.git`
   - Rama: `main` o `master`

2. **Configuración del Build:**
   - Tipo: **Docker Compose**
   - Docker Compose File: `docker-compose.yml`
   - (EasyPanel detectará automáticamente el archivo)

3. **Variables de Entorno en EasyPanel:**
   ```
   # Base de datos
   DB_USER=postgres
   DB_PASSWORD=tu_password_seguro
   DB_NAME=indicadores
   DB_PORT=5432
   
   # Backend
   BACKEND_PORT=8000
   
   # Frontend
   PORT=4173
   NODE_ENV=production
   VITE_SUPABASE_URL=https://tu-proyecto.supabase.co
   VITE_SUPABASE_ANON_KEY=tu-clave-anon
   ```

4. **Importante - Preparar el backend:**
   - Ejecuta `./setup-backend.sh ~/Downloads/Camara_de_comercio` para copiar el backend
   - El backend se copia directamente en la raíz del repositorio
   - El archivo `requirements.txt` debe existir en la raíz
   - El archivo `Dockerfile.backend` ya está incluido

5. **Puertos:**
   - Frontend: `4173`
   - Backend: `8000`
   - PostgreSQL: `5432` (solo interno, no exponer)

6. **Desplegar:**
   - Guardar configuración
   - Hacer clic en "Deploy"
   - EasyPanel construirá y levantará los 3 servicios automáticamente

### Opción 3: Despliegue con Docker (Solo Frontend)

Si solo necesitas el frontend sin backend:

```bash
# 1. Construir la imagen Docker
docker build -t camara-vlc-app .

# 2. Ejecutar el contenedor
docker run -d \
  -p 4173:4173 \
  --name camara-vlc-app \
  --env-file .env \
  camara-vlc-app

# 3. Ver logs
docker logs -f camara-vlc-app
```

### Opción 3: Despliegue Manual con Vite Preview

```bash
# 1. Construir para producción
npm run build

# 2. Iniciar servidor de preview
npm run start

# La aplicación estará disponible en http://localhost:4173
```

### Opción 4: Despliegue con Nginx (Producción)

1. **Construir la aplicación:**
   ```bash
   npm run build
   ```

2. **Configurar Nginx:**
   ```nginx
   server {
       listen 80;
       server_name tu-dominio.com;

       root /ruta/al/proyecto/dist;
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;
       }

       # Cache para assets estáticos
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

3. **Reiniciar Nginx:**
   ```bash
   sudo systemctl restart nginx
   ```

### Verificación Post-Despliegue

#### 1. Verificar servicios Docker

```bash
# Ver estado de todos los servicios
docker-compose ps

# Deberías ver 3 servicios corriendo:
# - frontend (ecosistema-valencia-view)
# - backend (app_backend)
# - db (db_indicadores)
```

#### 2. Verificar Backend

```bash
# Verificar que el backend responde
curl http://localhost:8000/api/v1/indicadores-disponibles

# Ver documentación de la API
# Abre en el navegador: http://localhost:8000/docs
```

#### 3. Verificar Base de Datos

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U postgres -d indicadores

# Verificar tablas
\dt

# Salir
\q
```

#### 4. Verificar Frontend

```bash
# Verificar que el frontend carga
curl http://localhost:4173
```

#### 5. Verificar en el navegador

- Abre la URL de producción (http://localhost:4173 o tu dominio)
- Verifica que no haya errores en la consola (F12)
- Verifica que los archivos JS/CSS se cargan correctamente
- Prueba la autenticación
- Verifica que las páginas principales funcionan:
  - `/dashboard` - Dashboard principal
  - `/kpis` - Dashboard de KPIs
  - `/tendencias` - Gráficos de tendencias (debe usar el backend)
  - `/brainnova-score` - Calculadora de Brainnova Score (debe usar el backend)

#### 6. Verificar conexión Frontend-Backend

- Ve a `/config` como administrador
- Verifica el estado del backend (debe mostrar "Conectado")
- Prueba la funcionalidad de actualización de datos
- Verifica que `/tendencias` muestra datos del backend
- Verifica que `/brainnova-score` puede calcular scores

## 🔧 Configuración de Base de Datos

### Migraciones de Supabase

Las migraciones se encuentran en `supabase/migrations/`. Para aplicarlas:

1. **Usando Supabase CLI:**
   ```bash
   supabase db push
   ```

2. **Manualmente desde el Dashboard:**
   - Ve al SQL Editor en Supabase
   - Ejecuta los archivos SQL en orden cronológico

### Carga de Datos Inicial

Para cargar datos de Brainnova en Supabase:

```bash
# Ver documentación detallada en:
scripts/README-load-database.md

# Script principal:
python scripts/load-all-data.py
```

## 🐛 Troubleshooting

### Error: "Port already in use"
```bash
# Encontrar el proceso usando el puerto
lsof -ti:4173

# Matar el proceso
kill -9 $(lsof -ti:4173)
```

### Error: "Cannot find module"
```bash
# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

### Error: "Build failed"
```bash
# Limpiar y reconstruir
rm -rf dist node_modules
npm install
npm run build
```

### Error: "Supabase connection failed"
- Verifica que `VITE_SUPABASE_URL` y `VITE_SUPABASE_ANON_KEY` estén correctamente configuradas
- Verifica que las políticas RLS permitan el acceso necesario
- Revisa la consola del navegador para errores específicos

### Error: "Backend not available"
- La aplicación tiene fallback automático a Supabase
- Si necesitas el backend, verifica que esté corriendo y accesible
- Configura `VITE_API_BASE_URL` correctamente

### Gráficos no muestran datos
- Verifica que haya datos en `resultado_indicadores` en Supabase
- Consulta `scripts/README-indicadores-con-datos.md` para encontrar indicadores con datos
- Verifica que los filtros seleccionados tengan datos disponibles

## 📝 Notas Importantes

1. **Puerto por defecto:** 
   - Desarrollo: `8080`
   - Producción: `4173`

2. **Archivos estáticos:** 
   - Después de `npm run build`, los archivos están en la carpeta `dist/`

3. **Variables de entorno:**
   - Las variables `VITE_*` se inyectan en tiempo de build
   - Si cambias variables de entorno, debes reconstruir la aplicación

4. **Docker:**
   - El Dockerfile usa multi-stage build para optimizar el tamaño de la imagen

5. **Seguridad:**
   - Nunca commitees archivos `.env` con credenciales
   - Usa variables de entorno del sistema o servicios de gestión de secretos

## 📚 Documentación Adicional

- `DEPLOY.md` - Instrucciones detalladas de despliegue
- `DOCKER.md` - Guía de despliegue con Docker
- `EASYPANEL.md` - Configuración específica para EasyPanel
- `scripts/README-load-database.md` - Carga de datos en Supabase
- `scripts/README-backend.md` - Configuración del backend de Brainnova
- `scripts/README-indicadores-con-datos.md` - Cómo encontrar indicadores con datos

## Licencia

Este proyecto es propiedad de la Cámara de Comercio de Valencia.
