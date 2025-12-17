<p align="center">
  <img src="https://img.shields.io/badge/Django-5.2.5-green?style=for-the-badge&logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-Neon-blue?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

# 🌱 Semillitas Ampiu API

> **API REST educativa para la enseñanza del idioma Ampiu** - Una lengua indígena colombiana preservada a través de la tecnología.

Backend robusto desarrollado en Django que potencia un juego educativo interactivo. Gestiona autenticación JWT, vocabulario por niveles, evaluaciones dinámicas y seguimiento del progreso de aprendizaje.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Docker](#-docker)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## ✨ Características

| Característica                 | Descripción                                                             |
| ------------------------------ | ----------------------------------------------------------------------- |
| 🔐 **Autenticación JWT**       | Tokens seguros con claims personalizados (rol, id, nombre)              |
| 👥 **Roles de Usuario**        | Administradores (email) y Jugadores (username) con flujos diferenciados |
| 📚 **Gestión de Vocabulario**  | Estructura jerárquica: Niveles → Palabras → Ejercicios                  |
| 📝 **Sistema de Evaluaciones** | Evaluaciones dinámicas con seguimiento de puntajes                      |
| 📊 **Seguimiento de Progreso** | Historial de palabras recolectadas y resultados                         |
| 📧 **Integración de Email**    | Envío automático de credenciales vía SendGrid                           |
| 🔍 **Filtros Avanzados**       | Filtrado por querystring con django-filter                              |

---

## 🏗 Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Frontend)                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API REST (Django + DRF)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  JWT Auth   │  │  Serializers │  │  Generic API Views     │  │
│  │  (Login)    │  │  (Validation)│  │  (CRUD Operations)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │ ORM
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL (Neon Tech)                        │
│  Usuario │ Nivel │ Palabra │ Evaluacion │ Ejercicio │ Resultado │
└─────────────────────────────────────────────────────────────────┘
```

### Modelo de Datos

```
Usuario (AbstractUser)
    ├── rol: 'Admin' | 'Jugador'
    ├── fecha_nacimiento
    └── email (único para Admin)

Nivel
    └── Palabra (FK → Nivel)
            └── Ejercicio (FK → Palabra, Evaluacion)

Evaluacion (FK → Nivel)
    ├── EvaluacionUsuarios (FK → Usuario)
    └── ResultadoEvaluaciones (FK → Usuario)

UsuarioPalabras (FK → Usuario, Palabra)
    └── Registro de palabras recolectadas
```

---

## 🛠 Tecnologías

| Categoría         | Tecnología            | Versión |
| ----------------- | --------------------- | ------- |
| **Framework**     | Django                | 5.2.5   |
| **API**           | Django REST Framework | 3.16    |
| **Base de Datos** | PostgreSQL (Neon)     | 15+     |
| **Autenticación** | Simple JWT            | 5.3+    |
| **Filtros**       | django-filter         | 24.3    |
| **Email**         | SendGrid              | 6.11    |
| **Testing**       | Pytest + Requests     | 9.0+    |
| **Contenedores**  | Docker + Compose      | 24+     |

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python** 3.13 o superior
- **pip** (gestor de paquetes de Python)
- **Git** para clonar el repositorio
- **PostgreSQL** (o cuenta en [Neon Tech](https://neon.tech/))
- **Docker** y **Docker Compose** (opcional, para despliegue)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/semillitas-ampiu/SemillitasAmpiu-Api.git
cd SemillitasAmpiu-Api
```

### 2. Crear entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (ver sección [Configuración](#-configuración)).

### 5. Ejecutar migraciones

```bash
cd project_semillitas
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

✅ La API estará disponible en: **http://localhost:8000**

---

## ⚙ Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# ═══════════════════════════════════════════════════════════════
# BASE DE DATOS (PostgreSQL - Neon Tech)
# ═══════════════════════════════════════════════════════════════
NEON_DB_NAME=semillitas_db
NEON_DB_USER=tu_usuario
NEON_DB_PASSWORD=tu_contraseña_segura
NEON_DB_HOST=ep-xxx-xxx-123456.us-east-2.aws.neon.tech
NEON_DB_PORT=5432

# ═══════════════════════════════════════════════════════════════
# SEGURIDAD
# ═══════════════════════════════════════════════════════════════
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
DEBUG=1  # Cambiar a 0 en producción

# ═══════════════════════════════════════════════════════════════
# EMAIL (SendGrid)
# ═══════════════════════════════════════════════════════════════
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **Importante**: Nunca subas el archivo `.env` al repositorio. Está incluido en `.gitignore`.

---

## 📖 Uso

### Autenticación

**Obtener token (Login):**

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "mi_usuario", "password": "mi_contraseña"}'
```

**Respuesta:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "mi_usuario",
    "rol": "Jugador"
  }
}
```

### Crear un Jugador

```bash
curl -X POST http://localhost:8000/api/jugador/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_jugador",
    "fecha_nacimiento": "2010-05-15"
  }'
```

> 💡 **Nota**: Si no se envía password, se usa el username como contraseña por defecto.

### Crear un Administrador

```bash
curl -X POST http://localhost:8000/api/administrador/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "fecha_nacimiento": "1990-01-01"
  }'
```

> 📧 El sistema genera una contraseña automática y la envía al email proporcionado.

---

## 🔌 API Endpoints

### Autenticación

| Método | Endpoint             | Descripción                |
| ------ | -------------------- | -------------------------- |
| `POST` | `/api/token/`        | Obtener tokens JWT (login) |
| `POST` | `/api/token/refresh` | Refrescar token de acceso  |

### Usuarios

| Método   | Endpoint                  | Descripción              |
| -------- | ------------------------- | ------------------------ |
| `GET`    | `/api/administrador/`     | Listar administradores   |
| `POST`   | `/api/administrador/`     | Crear administrador      |
| `GET`    | `/api/administrador/{id}` | Obtener administrador    |
| `PUT`    | `/api/administrador/{id}` | Actualizar administrador |
| `DELETE` | `/api/administrador/{id}` | Eliminar administrador   |
| `GET`    | `/api/jugador/`           | Listar jugadores         |
| `POST`   | `/api/jugador/`           | Crear jugador            |
| `GET`    | `/api/jugador/{id}`       | Obtener jugador          |
| `PUT`    | `/api/jugador/{id}`       | Actualizar jugador       |
| `DELETE` | `/api/jugador/{id}`       | Eliminar jugador         |

### Contenido Educativo

| Método | Endpoint           | Descripción                     |
| ------ | ------------------ | ------------------------------- |
| `GET`  | `/api/nivel/`      | Listar niveles de dificultad    |
| `GET`  | `/api/palabra/`    | Listar palabras del vocabulario |
| `POST` | `/api/palabra/`    | Crear nueva palabra             |
| `GET`  | `/api/evaluacion/` | Listar evaluaciones             |
| `POST` | `/api/evaluacion/` | Crear evaluación                |
| `GET`  | `/api/ejercicio/`  | Listar ejercicios               |
| `POST` | `/api/ejercicio/`  | Crear ejercicio                 |

### Progreso del Usuario

| Método | Endpoint            | Descripción                   | Filtros                |
| ------ | ------------------- | ----------------------------- | ---------------------- |
| `GET`  | `/api/recoleccion/` | Palabras recolectadas         | `?usuario=X&palabra=Y` |
| `POST` | `/api/recoleccion/` | Registrar palabra recolectada | -                      |
| `GET`  | `/api/resultado/`   | Resultados de evaluaciones    | `?usuario=X`           |
| `POST` | `/api/resultado/`   | Registrar resultado           | -                      |
| `GET`  | `/api/evaluado/`    | Evaluaciones realizadas       | -                      |

---

## 🧪 Testing

El proyecto incluye una suite completa de tests automatizados.

### Ejecutar todos los tests

```bash
# Asegúrate de que el servidor esté corriendo en otra terminal
cd project_semillitas
python manage.py runserver

# En otra terminal, ejecuta los tests
pytest test/ -v
```

### Ejecutar tests específicos

```bash
# Solo tests de autenticación
pytest test/test_token.py -v

# Solo tests de jugador
pytest test/test_jugador.py -v

# Solo tests de palabras
pytest test/test_palabra.py -v
```

### Cobertura de Tests

| Módulo        | Tests | Cobertura              |
| ------------- | ----- | ---------------------- |
| Token (JWT)   | 6     | Login, refresh, claims |
| Administrador | 10    | CRUD completo          |
| Jugador       | 10    | CRUD completo          |
| Palabra       | 10    | CRUD + unicidad        |
| Recolección   | 10    | CRUD + filtros         |
| Resultado     | 10    | CRUD + filtros         |

---

## 🐳 Docker

### Construcción y ejecución

```bash
# Construir y ejecutar
docker compose up --build

# Ejecutar en segundo plano
docker compose up -d

# Ver logs
docker compose logs -f

# Detener
docker compose down
```

### Archivo docker-compose.yml

El proyecto incluye configuración para:

- Servidor Django con Gunicorn
- Puerto expuesto: 8000
- Variables de entorno desde `.env`

---

## 📂 Estructura del Proyecto

```
SemillitasAmpiu-Api/
│
├── 📁 project_semillitas/          # Proyecto Django
│   ├── 📁 app_semillitas/          # Aplicación principal
│   │   ├── models.py               # Modelos de datos
│   │   ├── serializers.py          # Serializers DRF
│   │   ├── viewsApi.py             # Vistas de la API
│   │   ├── urlsApi.py              # Rutas de la API
│   │   ├── views.py                # Utilidades (email, password)
│   │   └── templates/              # Templates de email
│   │
│   ├── 📁 project_semillitas/      # Configuración
│   │   ├── settings.py             # Configuración Django
│   │   ├── urls.py                 # URLs raíz
│   │   └── wsgi.py                 # WSGI config
│   │
│   └── manage.py                   # CLI Django
│
├── 📁 test/                        # Tests automatizados
│   ├── conftest.py                 # Fixtures compartidos
│   ├── test_token.py               # Tests de autenticación
│   ├── test_administrador.py       # Tests de admin
│   ├── test_jugador.py             # Tests de jugador
│   ├── test_palabra.py             # Tests de palabras
│   ├── test_recoleccion.py         # Tests de recolección
│   ├── test_resultado.py           # Tests de resultados
│   └── cleanup_test_data.py        # Script de limpieza
│
├── 📁 docs/                        # Documentación
│   ├── PLAN_PRUEBAS_API.md         # Plan de pruebas
│   └── DOCKERIZACION_Y_DESPLIEGUE.md
│
├── .env.example                    # Ejemplo de variables de entorno
├── .gitignore                      # Archivos ignorados por Git
├── compose.yml                     # Docker Compose
├── Dockerfile                      # Imagen Docker
├── requirements.txt                # Dependencias Python
└── README.md                       # Este archivo
```

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. **Fork** el repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

### Guías de Estilo

- Sigue PEP 8 para código Python
- Escribe tests para nuevas funcionalidades
- Documenta los cambios en el código
- Mensajes de commit en español

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👥 Equipo

Desarrollado con ❤️ por el equipo de **Semillitas Ampiu** para la preservación y enseñanza del idioma Ampiu.

---

<p align="center">
  <strong>¿Preguntas o sugerencias?</strong><br>
  Abre un <a href="https://github.com/semillitas-ampiu/SemillitasAmpiu-Api/issues">Issue</a> en GitHub
</p>
