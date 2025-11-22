# Semillitas Ampiu API 🌱

Backend API for **Semillitas Ampiu**, an educational game designed to teach the Ampiu language. This RESTful API manages user authentication, vocabulary progression, evaluations, and score tracking for students and administrators.

## 🚀 Features

- **Role-Based Access Control**: Distinct flows for Administrators (email-based) and Players (username-based).
- **Vocabulary Management**: Hierarchical structure (Levels -> Words -> Exercises).
- **Evaluations System**: Dynamic assessments with score tracking.
- **Progress Tracking**: Detailed history of collected words and evaluation results.
- **Email Integration**: Automated credential delivery for administrators via SendGrid.
- **Secure Authentication**: JWT-based auth with custom claims.

## 🛠️ Tech Stack

- **Framework**: Django 5.2.5 & Django REST Framework 3.16
- **Database**: PostgreSQL (Neon Tech)
- **Authentication**: Simple JWT
- **Email Service**: SendGrid
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest & Requests

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.13+
- Docker & Docker Compose (optional)
- PostgreSQL database (or use SQLite for local dev)

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database (Neon PostgreSQL)
NEON_DB_NAME=your_db_name
NEON_DB_USER=your_db_user
NEON_DB_PASSWORD=your_db_password
NEON_DB_HOST=your_db_host
NEON_DB_PORT=5432

# Security & Email
SECRET_KEY=your_django_secret_key
DEBUG=1
SENDGRID_API_KEY=your_sendgrid_api_key
```

### Local Development

1. **Clone the repository**

   ```bash
   git clone https://github.com/semillitas-ampiu/SemillitasAmpiu-Api.git
   cd SemillitasAmpiu-Api
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```bash
   python project_semillitas/manage.py migrate
   ```

4. **Start the server**
   ```bash
   cd project_semillitas
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000`.

### 🐳 Docker Deployment

Run the application using Docker Compose:

```bash
docker compose up --build
```

## 🔌 API Endpoints

| Method   | Endpoint              | Description                |
| -------- | --------------------- | -------------------------- |
| POST     | `/api/token/`         | Obtain JWT Token (Login)   |
| POST     | `/api/token/refresh/` | Refresh JWT Token          |
| GET/POST | `/api/administrador/` | Manage Admins              |
| GET/POST | `/api/jugador/`       | Manage Players             |
| GET/POST | `/api/nivel/`         | Manage Difficulty Levels   |
| GET/POST | `/api/palabra/`       | Manage Vocabulary Words    |
| GET/POST | `/api/evaluacion/`    | Manage Assessments         |
| GET/POST | `/api/recoleccion/`   | Track User Collected Words |
| GET/POST | `/api/resultado/`     | Track Evaluation Scores    |

## 🧪 Testing

Tests are written using `pytest` and `requests` against the live server.

1. Ensure the server is running (`python manage.py runserver`).
2. Run tests:
   ```bash
   pytest test/
   ```

## 📂 Project Structure

```
project_semillitas/
├── app_semillitas/      # Main application logic
│   ├── models.py        # Custom User, Nivel, Palabra, etc.
│   ├── serializers.py   # DRF Serializers & Validation
│   ├── viewsApi.py      # API Views
│   └── urlsApi.py       # API Routes
├── project_semillitas/  # Project configuration
└── manage.py
```
