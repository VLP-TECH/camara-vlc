# Cámara de Comercio de Valencia - Plataforma Digital

Plataforma integral para el análisis, monitorización y desarrollo del ecosistema digital valenciano.

## Descripción

Esta aplicación proporciona una plataforma completa para:
- Análisis de indicadores económicos y KPIs
- Visualización de datos abiertos
- Gestión de encuestas y participación ciudadana
- Dashboard administrativo para gestión de usuarios

## Tecnologías

Este proyecto está construido con:

- **Vite** - Build tool y dev server
- **TypeScript** - Lenguaje de programación
- **React** - Biblioteca de UI
- **shadcn-ui** - Componentes de UI
- **Tailwind CSS** - Framework de estilos
- **Supabase** - Backend y autenticación

## Instalación

### Requisitos previos

- Node.js (versión 18 o superior) - [Instalar con nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
- npm o yarn

### Pasos de instalación

```sh
# Paso 1: Clonar el repositorio
git clone <YOUR_GIT_URL>

# Paso 2: Navegar al directorio del proyecto
cd camara-vlc

# Paso 3: Instalar las dependencias
npm install

# Paso 4: Configurar variables de entorno
# Crear archivo .env con las variables necesarias de Supabase

# Paso 5: Iniciar el servidor de desarrollo
npm run dev
```

## Scripts disponibles

- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Construye la aplicación para producción
- `npm run start` - Inicia el servidor de preview de producción

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
└── ...
```

## Despliegue

Consulta los archivos de documentación de despliegue:
- `DEPLOY.md` - Instrucciones generales de despliegue
- `DOCKER.md` - Despliegue con Docker
- `EASYPANEL.md` - Despliegue en EasyPanel

## Licencia

Este proyecto es propiedad de la Cámara de Comercio de Valencia.
