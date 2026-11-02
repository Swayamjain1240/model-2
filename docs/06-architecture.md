# Architecture Document

## 1. Document Information

| Field | Value |
|---|---|
| Project | Engineering-Focused Document RAG System |
| Version | 1.0 |
| Status | Draft |
| Audience | Developers and architects |

## 2. Architecture Summary

The MVP uses a modular-monolith architecture. A FastAPI process exposes the
application API, while a separate worker process handles document ingestion.
Both processes use shared persistence and provider interfaces.

## 3. Context View

```text
┌──────────┐       ┌────────────────────┐       ┌───────────────┐
│   User   │──────▶│ RAG application    │──────▶│ Model provider│
└──────────┘       │ API + worker       │       └───────────────┘
                   └─────────┬──────────┘
                             │
                             ▼
                    Database and file storage
```

The user interacts with the application. The application interacts with the
database, local file storage, cache/queue, and external embedding and LLM
providers.

## 4. Container View

### API process

Provides authentication, document APIs, query APIs, job status, health, and
metrics endpoints.

### Worker process

Consumes pending ingestion jobs and executes parsing, chunking, embedding, and
indexing.

### Database

Stores identity data, permissions, document metadata, chunks, vectors, jobs,
and query events.

### File storage

Stores original documents separately from searchable text.

### Cache and queue

Stores short-lived query results and supports asynchronous job coordination.

## 5. Runtime Topology Without Docker

```text
Local machine
├── FastAPI process
├── Background worker process
├── PostgreSQL process
└── Optional Redis-compatible process
```

The processes communicate over local network connections and are configured
through environment variables.

## 6. Security Boundaries

The API is the public boundary. Authentication occurs before protected
operations. Database queries include ownership or sharing filters. The
generation boundary receives only authorized, selected context. Secrets are
kept outside source control.

## 7. Scalability Path

The first version uses one API and one worker. If measurements justify it,
future versions may:

1. Add more worker processes.
2. Separate query and ingestion workloads.
3. Move original files to object storage.
4. Add a dedicated search service.
5. Add read replicas or partition large datasets.

These changes are postponed until load-test results identify a bottleneck.

## 8. Architecture Decisions

| Decision | Reason |
|---|---|
| Modular monolith | Keeps the MVP easy to develop and debug |
| Separate worker | Prevents long ingestion tasks from blocking APIs |
| Hybrid search | Handles both semantic meaning and exact technical terms |
| Permission-aware retrieval | Prevents unauthorized context leakage |
| Local deployment | Matches the current learning goal and excludes Docker |

## 9. Architecture Quality Checks

Before adding a new component, verify that it solves a measured problem,
has an owner, exposes health or failure behavior, and can be tested locally.
