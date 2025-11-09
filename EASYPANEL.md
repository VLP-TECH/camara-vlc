# 🚀 Guía de Configuración en Easypanel

## ⚠️ Error Común: Dockerfile Path

Si ves este error:
```
ERROR: resolve : lstat /etc/easypanel/projects/.../code/https:: no such file or directory
```

**Problema:** Easypanel está configurado con una URL de GitHub en lugar de la ruta del archivo.

## ✅ Configuración Correcta en Easypanel

### 1. Configuración del Repositorio

**URL del Repositorio:**
```
https://github.com/VLP-TECH/ecosistema-valencia-view.git
```

**Rama:**
```
main
```

### 2. Configuración del Dockerfile

**Ruta del Dockerfile:**
```
Dockerfile
```

**O dejar en blanco** (Easypanel buscará automáticamente `Dockerfile` en la raíz)

**❌ NO usar:**
- `https://github.com/VLP-TECH/ecosistema-valencia-view/blob/main/Dockerfile`
- `https:/github.com/...` (URLs web)

**✅ Usar:**
- `Dockerfile` (ruta relativa desde la raíz del repositorio)
- O dejar vacío

### 3. Configuración del Build

**Build Command:**
```
(Dejar vacío - el Dockerfile maneja el build)
```

**O si necesitas especificar:**
```bash
docker build -t app .
```

### 4. Configuración del Start

**Start Command:**
```
(Dejar vacío - el Dockerfile tiene CMD configurado)
```

**O si necesitas especificar:**
```bash
npm run start
```

### 5. Variables de Entorno

Configurar las siguientes variables en Easypanel:

```
NODE_ENV=production
PORT=4173
```

**Opcionales (si usas Supabase):**
```
VITE_SUPABASE_URL=tu-url-de-supabase
VITE_SUPABASE_ANON_KEY=tu-clave-anon
```

### 6. Puerto

**Puerto de la aplicación:**
```
4173
```

## 🔧 Pasos para Corregir el Error

1. **Ir a la configuración del proyecto en Easypanel**
2. **Buscar la sección "Dockerfile" o "Build Settings"**
3. **En el campo "Dockerfile Path":**
   - Eliminar cualquier URL de GitHub
   - Escribir solo: `Dockerfile`
   - O dejar el campo vacío
4. **Guardar los cambios**
5. **Redesplegar el proyecto**

## 📋 Verificación

Después de configurar, el build debería mostrar:
```
Step 1/XX : FROM node:18-alpine AS builder
...
```

En lugar de:
```
ERROR: resolve : lstat .../https:: no such file or directory
```

## 🐛 Troubleshooting

### Error: "Dockerfile not found"
- Verifica que el Dockerfile esté en la raíz del repositorio
- Verifica que el repositorio esté clonado correctamente
- Asegúrate de que la ruta sea `Dockerfile` (sin `/` al inicio)

### Error: "Build failed"
- Verifica que todas las dependencias estén en `package.json`
- Revisa los logs de build en Easypanel
- Verifica que Node.js 18 esté disponible

### Error: "Port already in use"
- Verifica que el puerto 4173 esté configurado correctamente
- Asegúrate de que no haya otro servicio usando el puerto

## 📝 Notas Importantes

- El Dockerfile está en la **raíz** del repositorio
- No uses URLs de GitHub para el Dockerfile
- Usa solo la ruta relativa: `Dockerfile`
- El Dockerfile usa multi-stage build para optimizar el tamaño
- La aplicación corre en el puerto **4173** por defecto


