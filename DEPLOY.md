# 🚀 Guía de Despliegue en Producción - Vite.js

## 📋 Opción 1: Usando `vite preview` (Recomendado para este proyecto)

### Pasos:

```bash
# 1. Instalar dependencias
npm install

# 2. Construir el proyecto para producción
npm run build

# 3. Iniciar servidor de preview
npm run start
# o directamente:
vite preview --host 0.0.0.0 --port 4173
```

---

## 📋 Opción 2: Usando `serve` (Alternativa)

### Pasos:

```bash
# 1. Instalar dependencias
npm install

# 2. Construir el proyecto
npm run build

# 3. Instalar serve globalmente
npm install -g serve

# 4. Servir los archivos estáticos
serve -s dist -l 4173 --cors
```

---

## 📋 Opción 3: Usando Docker (Como está configurado)

### Pasos:

```bash
# 1. Construir la imagen Docker
docker build -t ecosistema-valencia-view .

# 2. Ejecutar el contenedor
docker run -d -p 4173:4173 --name ecosistema-valencia-view ecosistema-valencia-view

# 3. Ver logs
docker logs -f ecosistema-valencia-view
```

---

## 📋 Opción 4: Usando Supervisor

### Crear archivo de configuración `/etc/supervisor/conf.d/ecosistema-valencia.conf`:

```ini
[program:ecosistema-valencia]
command=npm run start
directory=/ruta/completa/al/proyecto
user=tu-usuario
autostart=true
autorestart=true
stderr_logfile=/var/log/ecosistema-valencia.err.log
stdout_logfile=/var/log/ecosistema-valencia.out.log
environment=NODE_ENV="production",PORT="4173"
```

### Comandos Supervisor:

```bash
# 1. Construir el proyecto
cd /ruta/al/proyecto
npm install
npm run build

# 2. Recargar configuración de supervisor
sudo supervisorctl reread
sudo supervisorctl update

# 3. Iniciar el servicio
sudo supervisorctl start ecosistema-valencia

# 4. Ver estado
sudo supervisorctl status ecosistema-valencia

# 5. Reiniciar
sudo supervisorctl restart ecosistema-valencia
```

---

## 🔧 Variables de Entorno

Asegúrate de configurar las variables de entorno necesarias:

```bash
NODE_ENV=production
PORT=4173
```

---

## ✅ Verificación Post-Despliegue

1. **Verificar que la aplicación carga:**
   ```bash
   curl http://localhost:4173
   ```

2. **Verificar en el navegador:**
   - Abre `http://tu-servidor:4173`
   - Verifica que no haya errores en la consola (F12)
   - Verifica que los archivos JS/CSS se cargan correctamente

---

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

---

## 📝 Notas Importantes

1. **Puerto por defecto:** El proyecto está configurado para usar el puerto 4173
2. **Archivos estáticos:** Después de `npm run build`, los archivos están en la carpeta `dist/`
3. **Docker:** El Dockerfile usa multi-stage build para optimizar el tamaño de la imagen
