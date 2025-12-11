# 🐳 Informe de Dockerización y Despliegue en Render

## Semillitas Ampiu API

**Fecha:** Diciembre 2025  
**Proyecto:** API REST educativa para enseñar el idioma Ampiu  
**Stack:** Django 5.2.5 + PostgreSQL (Neon) + Gunicorn

---

## 📋 Índice

1. [Requisitos Previos](#1-requisitos-previos)
2. [Estructura del Proyecto](#2-estructura-del-proyecto)
3. [Configuración del Dockerfile](#3-configuración-del-dockerfile)
4. [Configuración de Docker Compose](#4-configuración-de-docker-compose)
5. [Variables de Entorno](#5-variables-de-entorno)
6. [Construcción y Pruebas Locales](#6-construcción-y-pruebas-locales)
7. [Preparación para Render](#7-preparación-para-render)
8. [Despliegue en Render](#8-despliegue-en-render)
9. [Verificación del Despliegue](#9-verificación-del-despliegue)
10. [Solución de Problemas Comunes](#10-solución-de-problemas-comunes)

---

## 1. Requisitos Previos

### Software necesario

- **Docker Desktop** (v20.10+)
- **Docker Compose** (v2.0+)
- **Git** para control de versiones
- **Cuenta en GitHub** (repositorio del proyecto)
- **Cuenta en Render** (https://render.com)
- **Base de datos PostgreSQL** (Neon Tech recomendado)

### Verificar instalación de Docker

```bash
docker --version
docker compose version
```

---

## 2. Estructura del Proyecto

```
SemillitasAmpiu-Api/
├── Dockerfile              # Configuración de imagen Docker
├── compose.yml             # Orquestación de servicios
├── requirements.txt        # Dependencias Python
├── .env                    # Variables de entorno (NO subir a Git)
├── .gitignore
└── project_semillitas/     # Proyecto Django
    ├── manage.py
    ├── app_semillitas/     # Aplicación principal
    └── project_semillitas/ # Configuración Django
```

---

## 3. Configuración del Dockerfile

### Estrategia Multi-Stage Build

Se utiliza un **build multi-etapa** para optimizar el tamaño de la imagen final:

```dockerfile
# Stage 1: Base build stage
FROM python:3.13-slim AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema necesarias para mysqlclient y psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Establece el directorio de trabajo del proyecto Django
WORKDIR /app/project_semillitas

# Expose the application port
EXPOSE 8000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "project_semillitas.wsgi:application"]
```

### Explicación de las etapas

| Etapa          | Propósito                                                                       |
| -------------- | ------------------------------------------------------------------------------- |
| **Builder**    | Instala compiladores y dependencias de desarrollo para compilar paquetes Python |
| **Production** | Imagen limpia solo con runtime necesario, sin herramientas de compilación       |

### Beneficios del Multi-Stage

- ✅ Imagen final más pequeña (~200MB vs ~800MB)
- ✅ Menor superficie de ataque (sin compiladores)
- ✅ Mejor caché de capas Docker
- ✅ Usuario no-root para seguridad

---

## 4. Configuración de Docker Compose

### Archivo `compose.yml`

```yaml
services:
  django-api:
    build: .
    container_name: semillitas-api
    ports:
      - '8000:8000'
    environment:
      NEON_DB_NAME: ${NEON_DB_NAME}
      NEON_DB_USER: ${NEON_DB_USER}
      NEON_DB_PASSWORD: ${NEON_DB_PASSWORD}
      NEON_DB_HOST: ${NEON_DB_HOST}
      NEON_DB_PORT: ${NEON_DB_PORT}
      SECRET_KEY: ${SECRET_KEY}
      SENDGRID_API_KEY: ${SENDGRID_API_KEY}
    env_file:
      - .env
    volumes:
      - ./project_semillitas:/app/project_semillitas
    develop:
      watch:
        - action: sync
          path: ./project_semillitas
          target: /app/project_semillitas
          ignore:
            - __pycache__/
            - '*.pyc'
            - '*.pyo'
            - db.sqlite3
        - action: rebuild
          path: ./requirements.txt
```

### Características del compose.yml

- **Hot reload** con `docker compose watch` para desarrollo
- **Variables de entorno** cargadas desde `.env`
- **Volúmenes** para sincronizar código en desarrollo

---

## 5. Variables de Entorno

### Crear archivo `.env` en la raíz del proyecto

```env
# Base de datos PostgreSQL (Neon Tech)
NEON_DB_NAME=semillitas_db
NEON_DB_USER=tu_usuario
NEON_DB_PASSWORD=tu_password_seguro
NEON_DB_HOST=ep-xxx.us-east-2.aws.neon.tech
NEON_DB_PORT=5432

# Seguridad Django
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura
DEBUG=0

# Email (SendGrid)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxx
```

### ⚠️ Importante

- **NUNCA** subir `.env` a Git
- Agregar `.env` al `.gitignore`
- En producción, `DEBUG=0`

---

## 6. Construcción y Pruebas Locales

### Paso 1: Construir la imagen

```bash
# Construir imagen desde el Dockerfile
docker compose build

# O construir sin caché (si hay problemas)
docker compose build --no-cache
```

### Paso 2: Levantar el contenedor

```bash
# Iniciar en modo detached (background)
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f
```

### Paso 3: Ejecutar migraciones

```bash
# Acceder al contenedor
docker compose exec django-api bash

# Dentro del contenedor, ejecutar migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser
```

### Paso 4: Verificar funcionamiento

```bash
# Probar endpoint de salud
curl http://localhost:8000/

# Probar API
curl http://localhost:8000/api/nivel/
```

### Paso 5: Detener contenedores

```bash
# Detener y eliminar contenedores
docker compose down

# Detener y eliminar también volúmenes
docker compose down -v
```

---

## 7. Preparación para Render

### 7.1 Verificar archivos necesarios

Asegurarse de que existan en el repositorio:

- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `.gitignore` (con `.env` incluido)

### 7.2 Configurar ALLOWED_HOSTS

En `project_semillitas/project_semillitas/settings.py`:

```python
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",  # Permite todos los subdominios de Render
]
```

### 7.3 Configurar archivos estáticos (si aplica)

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 7.4 Subir código a GitHub

```bash
git add .
git commit -m "Preparar para despliegue en Render"
git push origin main
```

---

## 8. Despliegue en Render

### Paso 1: Crear cuenta y proyecto

1. Ir a [https://render.com](https://render.com)
2. Registrarse/Iniciar sesión con GitHub
3. Click en **"New +"** → **"Web Service"**

### Paso 2: Conectar repositorio

1. Seleccionar **"Build and deploy from a Git repository"**
2. Conectar cuenta de GitHub si no está conectada
3. Buscar y seleccionar el repositorio `SemillitasAmpiu-Api`
4. Click en **"Connect"**

### Paso 3: Configurar el servicio

| Campo             | Valor                               |
| ----------------- | ----------------------------------- |
| **Name**          | `semillitas-ampiu-api`              |
| **Region**        | `Oregon (US West)` o el más cercano |
| **Branch**        | `main`                              |
| **Runtime**       | `Docker`                            |
| **Instance Type** | `Free` (para pruebas) o `Starter`   |

### Paso 4: Configurar variables de entorno

En la sección **"Environment Variables"**, agregar:

| Key                | Value                      |
| ------------------ | -------------------------- |
| `NEON_DB_NAME`     | `tu_nombre_db`             |
| `NEON_DB_USER`     | `tu_usuario`               |
| `NEON_DB_PASSWORD` | `tu_password`              |
| `NEON_DB_HOST`     | `ep-xxx.neon.tech`         |
| `NEON_DB_PORT`     | `5432`                     |
| `SECRET_KEY`       | `clave-secreta-produccion` |
| `DEBUG`            | `0`                        |
| `SENDGRID_API_KEY` | `SG.xxx`                   |

### Paso 5: Configuración avanzada (opcional)

- **Health Check Path:** `/`
- **Auto-Deploy:** `Yes` (despliega automáticamente con cada push)

### Paso 6: Desplegar

1. Click en **"Create Web Service"**
2. Esperar a que Render construya la imagen Docker
3. El proceso toma aproximadamente 5-10 minutos

### Paso 7: Ejecutar migraciones en Render

Después del primer despliegue, ir a la pestaña **"Shell"** en Render:

```bash
cd /app/project_semillitas
python manage.py migrate
```

---

## 9. Verificación del Despliegue

### URL del servicio

Una vez desplegado, Render proporciona una URL como:

```
https://semillitas-ampiu-api.onrender.com
```

### Pruebas de verificación

```bash
# Verificar que el servidor responde
curl https://semillitas-ampiu-api.onrender.com/

# Probar endpoint de API
curl https://semillitas-ampiu-api.onrender.com/api/nivel/

# Probar autenticación JWT
curl -X POST https://semillitas-ampiu-api.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Verificar logs en Render

1. Ir al dashboard de Render
2. Seleccionar el servicio
3. Click en pestaña **"Logs"**
4. Revisar errores o advertencias

---

## 10. Solución de Problemas Comunes

### Error: "No module named 'app_semillitas'"

**Causa:** El WORKDIR no apunta al directorio correcto.  
**Solución:** Verificar que el Dockerfile tenga:

```dockerfile
WORKDIR /app/project_semillitas
```

### Error: "Connection refused" a la base de datos

**Causa:** Variables de entorno no configuradas correctamente.  
**Solución:**

1. Verificar variables en Render Dashboard
2. Asegurar que Neon permite conexiones desde cualquier IP

### Error: "ALLOWED_HOSTS"

**Causa:** El dominio de Render no está permitido.  
**Solución:** Agregar `.onrender.com` a ALLOWED_HOSTS:

```python
ALLOWED_HOSTS = ["*"]  # Solo para debugging
# O específicamente:
ALLOWED_HOSTS = [".onrender.com"]
```

### La aplicación se "duerme" en el plan gratuito

**Causa:** Render Free tier suspende servicios inactivos después de 15 minutos.  
**Solución:**

- Upgrade a plan Starter ($7/mes)
- O usar un servicio de ping como UptimeRobot

### Error de SSL con PostgreSQL

**Causa:** Neon requiere SSL.  
**Solución:** Verificar en `settings.py`:

```python
DATABASES = {
    'default': {
        # ... otras configuraciones
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}
```

---

## 📊 Resumen del Flujo de Despliegue

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Desarrollo     │     │    GitHub       │     │     Render      │
│    Local        │────▶│   Repository    │────▶│   Web Service   │
│  (Docker)       │     │                 │     │   (Docker)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                                               │
        │                                               │
        ▼                                               ▼
┌─────────────────┐                           ┌─────────────────┐
│  docker compose │                           │   Neon Tech     │
│     up --build  │                           │   PostgreSQL    │
└─────────────────┘                           └─────────────────┘
```

---

## 🔗 Referencias

- [Documentación Docker](https://docs.docker.com/)
- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Neon PostgreSQL](https://neon.tech/docs)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)

---

**Autor:** Equipo Semillitas Ampiu  
**Última actualización:** Diciembre 2025
