# FastAPI + SQLModel Starter

Production‑ready starter for building APIs with **FastAPI**, SQLModel, and pydantic‑settings, using SQLite for development and PostgreSQL for production.

## Features

- FastAPI with async SQLModel and dependency injection.
- SQLite for local development, PostgreSQL for production.
- Alembic migrations wired to SQLModel metadata.
- Environment‑based configuration with pydantic‑settings and `.env` files.
- Basic example CRUD endpoint (`User`) and API versioning scaffold.
- Ready to containerize with Docker and orchestrate via `docker-compose` (optional).

## Getting started

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environments

Create `.env` for development (SQLite):

```env
ENV=dev
ASYNC_DB_URL=sqlite+aiosqlite:///../db.sqlite3
```

Create `.env` for production (PostgreSQL):

```env
ENV=prod
ASYNC_DB_URL=postgresql+psycopg://user:password@db:5432/app_db
```

### 3. Run the app (dev)

```bash
uvicorn app.main:app --reload
```

- API docs: `http://localhost:8000/docs`
- Health check or example endpoints live under `/api/v1/...` as defined in the routers.[3]

On production, run the same commands in your container or CI/CD pipeline against PostgreSQL.

## Development workflow

- Add or update SQLModel models in `app/models/`.
- Implement business logic in `app/services/` and expose endpoints via routers in `app/api/v1/`.
- Write tests in `tests/` using `pytest` and `httpx` for API calls, following patterns from SQLModel + FastAPI tutorials.

You can extend this starter with authentication (JWT), better logging, structured settings per environment, and Docker‑based local stacks using patterns from existing FastAPI + SQLModel template repositories.
