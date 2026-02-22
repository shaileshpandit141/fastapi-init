# FastAPI Starter Template

Production-ready **FastAPI** starter template for building scalable APIs with:

* **Async SQLModel ORM**
* **Pydantic Settings**
* **Modular architecture** (feature-based)
* **Service + Repository + Policy pattern**
* **Role-Based Access Control (RBAC)**
* **SQLite for development & PostgreSQL for production**

This template is designed to be **testable, maintainable, and etc**, with clear separation of concerns for large projects.

## 🚀 Features

* **FastAPI** fully async with dependency injection.
* **SQLModel** for ORM with Alembic migrations.
* **Modular architecture**: each module (users, auth, roles, permissions, etc.) contains:

  * API routes
  * Services (business logic)
  * Repositories (DB access)
  * Policies (authorization rules)
  * Schemas (request/response DTOs)

* **RBAC with policy engine**: user, role, and permission management.
* **UnitOfWork pattern** for transactional integrity.
* **Environment-based configuration** via `.env` files.
* **Docker-ready**: easy containerization & orchestration.
* **Test-ready**: layered tests with unit, integration, API, and optional E2E tests.
* **Type-safe**: Enums for roles and permissions, making code safer and self-documenting.
* **Async-friendly**: fully compatible with background tasks and async workflows.

## 📁 Project App Structure

```text
app
├── __init__.py
├── main.py
├── adapters
│   ├── db
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── _mixins.py
│   │   │   ├── permission.py
│   │   │   ├── role_permission.py
│   │   │   ├── role.py
│   │   │   ├── user.py
│   │   │   └── user_role.py
│   │   ├── session.py
│   │   └── unit_of_work.py
│   ├── email
│   ├── __init__.py
│   ├── messaging
│   │   ├── celery_app.py
│   │   ├── __init__.py
│   │   └── tasks
│   │       ├── email_tasks.py
│   │       ├── __init__.py
│   ├── rate_limit
│   ├── redis
│   └── security
│       ├── jwt
│       │   ├── __init__.py
│       │   ├── blocklist.py
│       │   ├── exceptions.py
│       │   ├── factory.py
│       │   ├── manager.py
│       │   └── verifier.py
│       ├── one_time_password
│       │   ├── __init__.py
│       │   └── generator.py
│       └── password
│           ├── hasher.py
│           └── __init__.py
├── cli
│   ├── __init__.py
│   ├── __main__.py
│   ├── seed
│   └── user
├── core
├── modules
│   ├── __init__.py
│   ├── router.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── routes.py
│   │   ├── policies
│   │   │   ├── __init__.py
│   │   │   ├── login.py
│   │   │   ├── register.py
│   │   ├── repositories
│   │   │   └── __init__.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── login.py
│   │   │   ├── register.py
│   │   └── services
│   │       ├── __init__.py
│   │       ├── login.py
│   │       └── register.py
│   ├── permissions
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── routes.py
│   │   ├── policies
│   │   │   ├── __init__.py
│   │   │   └── permission.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   └── permission.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   └── permission.py
│   │   └── services
│   │       ├── __init__.py
│   │       └── permission.py
│   ├── roles
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── routes.py
│   │   ├── __init__.py
│   │   ├── policies
│   │   │   ├── __init__.py
│   │   │   ├── role_permission.py
│   │   │   └── role.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   ├── role_permission.py
│   │   │   └── role.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── role_permission.py
│   │   │   └── role.py
│   │   └── services
│   │       ├── __init__.py
│   │       ├── role_permission.py
│   │       └── role.py
│   └── users
│       ├── dependencies.py
│       ├── exceptions.py
│       ├── routes.py
│       ├── __init__.py
│       ├── policies
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── user_role.py
│       ├── repositories
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── user_role.py
│       ├── schemas
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── user_role.py
│       └── services
│           ├── __init__.py
│           ├── user.py
│           └── user_role.py
└── shared
```

## ⚡ Getting Started

### Install dependencies

```bash
uv sync
```

### Configure environments

* Check **.env.sample** file for env vriables.
  * For dev env used (**.env**).
  * And for production use (**.env.pro**).

### Run the app

**Development:**

```bash
uv run uvicorn app.main:app --reload
```

* API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* Health check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
* And much more.

**Production:** run in container or via CI/CD pipeline against PostgreSQL.

## 🛠 Development Workflow

1. **Models:** Define ORM models inside `adapters/db/models/`.
2. **Repositories:** Implement DB operations in `modules/<feature>/repositories/`.
3. **Services:** Business logic lives in `modules/<feature>/services/`.
4. **Policies:** Authorization and RBAC rules in `modules/<feature>/policies/`.
5. **API Routes:** Expose endpoints via `modules/<feature>/api/routes.py`.
6. **Schemas:** Define request/response DTOs in `modules/<feature>/schemas/`.
7. **UnitOfWork:** Use for transactional control; repositories never commit directly.
8. **Testing:** Follow the layered testing structure:

```text
tests
├── api
│   └── users
│       └── test_user_routes.py
├── conftest.py
├── e2e
│   ├── test_auth_flow.py
│   ├── test_full_user_lifecycle.py
│   └── test_rbac_flow.py
├── integration
│   ├── db
│   └── users
└── unit
```

## 💾 Seeding Roles & Permissions

Roles and permissions are defined as **Enums** and seeded idempotently into the database:

* Role-Permission mapping is centralized in `app/cli/seed/`.
* Permissions are type-safe using `app/cli/seed/`.
* Seeder ensures DB stays in sync with code on each deployment.

Run seed command:

```bash
uv run python -m app.cli seed sync-role-permission
```

And for more commands run:

```bash
uv run python -m app.cli --help
```

## ✅ Best Practices

* **Services** contain business logic only, no HTTP or DB commits.
* **Repositories** handle only DB access, no business rules.
* **Policies** are pure and declarative.
* **Domain exceptions** (e.g., `UserAlreadyExists`) instead of generic exceptions.
* **DTOs (schemas)** always separate from ORM models.
* **Dependencies injected** for testability and modularity.
* **Unit tests** mock dependencies, integration tests use a test DB.

## 🧪 Testing

* Unit, integration, and API tests are organized per module.
* Use `tests/factories/` for Faker-based test data.
* Override dependencies in `tests/conftest.py` for isolation.
* E2E tests optional for full system verification.

## 📦 Docker

* Dockerfile & docker-compose ready for local dev + production.
* Environment-specific configuration via `.env`.
* Supports async workers & background tasks.

## 🤝 Contributing

Contributions are welcome! Please open an issue or PR for improvements.

## 👤 Author

**Shailesh Pandit**\
Email: 📧 [shaileshpandit141@gmail.com](mailto:shaileshpandit141@gmail.com)
