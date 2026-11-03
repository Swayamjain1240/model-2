# Phase 1: Foundation

## Status

Phase 1 establishes the locally runnable application foundation for the
engineering-focused RAG system.

## Completed Scope

- Python package and modular application structure
- Environment-based configuration
- FastAPI application factory
- Health endpoint
- JSON logging configuration
- Request correlation IDs
- SQLAlchemy database foundation
- Alembic migration configuration and initial schema
- Users, documents, permissions, jobs, and document chunks tables
- Password hashing using `scrypt`
- JWT access tokens
- Registration, login, and current-user endpoints
- Authentication dependency for protected routes
- Automated foundation and authentication tests
- Python line-count validation with a 200-line limit

## Local Commands

Install the project and development tools:

```text
python -m pip install -e ".[dev]"
```

Create or upgrade the local database:

```text
alembic upgrade head
```

Run the API:

```text
uvicorn app.main:app --reload
```

Run quality checks:

```text
ruff check app scripts tests
ruff format --check app scripts tests
python scripts/check_line_limits.py
pytest
```

## API Endpoints

```text
GET  /api/health
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

## Engineering Notes

The current local database default is SQLite so a new developer can run the
foundation without Docker. The schema is managed through Alembic rather than
depending on application startup to create tables. The test suite uses an
isolated in-memory database and does not write user data to the repository.

## Remaining Work

The foundation does not yet upload or process documents. The next phase will
add file validation, storage, asynchronous ingestion jobs, parsing, chunking,
and job status APIs.
