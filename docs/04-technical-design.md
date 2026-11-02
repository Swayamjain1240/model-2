# Technical Design Document

## 1. Document Information

| Field | Value |
|---|---|
| Project | Engineering-Focused Document RAG System |
| Version | 1.0 |
| Status | Draft |
| Audience | Implementing engineers |

## 2. Technical Direction

The initial implementation will use Python and FastAPI. PostgreSQL with a
vector extension is the target persistence layer because it can store regular
application data, vector embeddings, and keyword-search metadata together.
The API and worker run as separate local processes. Docker is not required.

## 3. Suggested Technology Stack

| Area | Technology or interface |
|---|---|
| Language | Python 3.11+ |
| API | FastAPI and Pydantic |
| ORM/data access | SQLAlchemy |
| Database | PostgreSQL with pgvector and full-text search |
| Authentication | Password hashing and JWT access tokens |
| File parsing | Format-specific parser adapters |
| Cache/queue | Redis-compatible interface; local fallback for development |
| Testing | pytest and HTTP client tests |
| Load testing | Locust |
| Observability | Structured logging, metrics, and tracing interfaces |

The provider choices may change after benchmarking. Application code should
depend on interfaces rather than provider-specific calls.

## 4. Database Design

### users

```text
id, email, password_hash, is_active, created_at, updated_at
```

### documents

```text
id, owner_id, filename, storage_path, content_hash,
mime_type, version, status, created_at, updated_at
```

### document_permissions

```text
document_id, user_id, role, created_at
```

Roles are initially `OWNER`, `EDITOR`, and `VIEWER`.

### ingestion_jobs

```text
id, document_id, status, attempts, error_code,
error_message, started_at, completed_at, created_at
```

### document_chunks

```text
id, document_id, chunk_index, text, page_number,
section, token_count, embedding, search_text, created_at
```

The combination of `document_id` and `chunk_index` should be unique for a
document version.

### query_events

```text
id, user_id, query_hash, result_count, cache_hit,
model_name, input_tokens, output_tokens, total_latency_ms, created_at
```

Do not store full confidential questions or document text in operational logs
unless explicitly configured for a protected development environment.

## 5. Chunking Design

The initial default is 500–800 tokens per chunk with 50–100 tokens of
overlap. Chunk metadata includes filename, page, section, document ID, and
chunk index. The chunker must keep headings with their following content when
possible and avoid splitting code blocks or tables unnecessarily.

Chunk settings are configuration values so that evaluation can compare
different strategies.

## 6. Retrieval Design

For a query:

1. Create the query embedding.
2. Run vector search for the top 20 candidates.
3. Run keyword search for the top 20 candidates.
4. Apply document permission filters in both searches.
5. Merge results using rank fusion.
6. Remove duplicate chunks.
7. Re-rank the candidate set.
8. Send the best 5–8 chunks to generation.

The exact values are configurable and must be validated by evaluation tests.

## 7. API Contract

### `POST /documents`

Uploads a document and returns a document ID and ingestion job ID.

### `GET /jobs/{job_id}`

Returns job status, progress information when available, and a safe error
summary when processing fails.

### `POST /queries`

Request:

```json
{
  "question": "How does authentication work?",
  "document_ids": ["doc_123"]
}
```

Response:

```json
{
  "answer": "Authentication uses ...",
  "citations": [
    {"document_id": "doc_123", "page": 2, "chunk_id": "chunk_10"}
  ],
  "metrics": {"total_latency_ms": 1840}
}
```

## 8. Cache Design

Cache keys include the user scope, normalized question, document version, and
retrieval configuration. A document version change invalidates answers based
on the old version. Cache entries have a TTL and must never bypass permission
checks.

## 9. Worker Design

The worker claims one pending job at a time during the first implementation.
The claim operation must prevent two workers from processing the same job.
Each stage reports progress and the worker records a failure category. The
worker may retry transient provider failures but should not retry invalid
documents indefinitely.

## 10. Observability Design

Every request and job receives a correlation ID. Timers are recorded for each
pipeline stage. Metrics use counters for requests and errors and histograms
for latency. Traces show API, database, retrieval, re-ranking, and model-call
boundaries.
