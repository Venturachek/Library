# 📚 Library Management System

A REST API for library management built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL**. Features JWT authentication, role-based access control, AI-powered support bot, and automated email reminders via AWS SES.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 17 |
| Migrations | Alembic |
| Cache | Redis + fastapi-cache |
| Task Queue | Celery + Celery Beat |
| Email | AWS SES |
| Auth | JWT (python-jose) |
| AI Bot | Telegram Bot (aiogram) + OpenAI-compatible API |
| Containerization | Docker + Docker Compose |

---

## ✨ Features

- **Book Management** — CRUD, bulk insert, filtering by title/author/genre, pagination
- **User Authentication** — Register, login, JWT tokens stored in cookies
- **Role-Based Access Control** — `admin` and `user` roles with protected endpoints
- **Book Loans** — Borrow and return books with automatic availability tracking
- **Email Reminders** — Celery Beat sends AWS SES reminders the day before a book is due
- **Redis Caching** — Book listings cached for fast response
- **AI Support Bot** — Telegram bot with function calling for book search and loan info
- **Repository + Service Pattern** — Clean architecture with DataMapper layer

---

## 🏗️ Project Structure

```
src/
├── api/           # FastAPI routers
├── models/        # SQLAlchemy ORM models
├── repositories/  # Database access layer
├── services/      # Business logic layer
├── schemas/       # Pydantic schemas
├── migration/     # Alembic migrations
├── ai/            # AI orchestrator + tools
└── task/          # Celery tasks
bot/               # Telegram bot
tests/             # pytest tests
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
MODE=LOCAL

DB_HOST=library_db
DB_PORT=5432
DB_USER=qwerty
DB_PASS=qwerty
DB_NAME=library

JWT_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30

REDIS_HOST=library_cache
REDIS_PORT=6379

AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=eu-central-1
SES_EMAIL_FROM=your@email.com
```

---

## 🐳 Running with Docker Compose

```bash
# Clone the repository
git clone https://github.com/Venturachek/Library.git
cd Library

# Create .env file (see above)

# Build and start all services
docker compose up --build

# Run migrations
docker exec library_back alembic upgrade head
```

---

## 🔧 Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn src.main:app --reload

# Start Celery worker (separate terminal)
celery --app=src.task.celery_app:celery_instance worker -l INFO

# Start Celery Beat (separate terminal)
celery --app=src.task.celery_app:celery_instance beat -l INFO
```

---

## 📖 API Documentation

After starting the server, open:

```
http://localhost:8000/docs
```

### Main Endpoints

| Method | Endpoint | Description | Access     |
|---|---|---|------------|
| POST | `/auth/register` | Register new user | Public     |
| POST | `/auth/login` | Login | Public     |
| GET | `/books` | Get all books | Public     |
| POST | `/books` | Add book | Admin      |
| POST | `/books/bulk` | Bulk add books | Admin      |
| PATCH | `/books/{id}` | Update book | Admin      |
| DELETE | `/books/{id}` | Delete book | Admin      |
| POST | `/loan/{book_id}` | Borrow book | Authorized |
| POST | `/loan/{loan_id}/return` | Return book | Admin      |

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📬 Email Reminders

Celery Beat automatically sends reminder emails via AWS SES to users whose books are due the next day.

---

## 🤖 AI Support Bot

The Telegram bot uses function calling to answer user questions about book availability and loan status in natural language.

---

## 📝 License

MIT