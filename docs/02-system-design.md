# System Design Document

## 1. Document Information

| Field | Value |
|---|---|
| Project | Engineering-Focused Document RAG System |
| Version | 1.0 |
| Status | Draft |
| Audience | Developers and system-design reviewers |

## 2. Purpose

This document describes the high-level system design for the document-based
RAG application. It explains the major components, data flow, system
boundaries, and engineering decisions without describing every class or
implementation detail.

## 3. Design Principles

- Start with a modular monolith rather than microservices.
- Keep ingestion and question answering as separate workflows.
- Make search, embedding, parser, and LLM providers replaceable.
- Enforce authorization before document content reaches retrieval context.
- Prefer measurable behavior over unverified claims.
- Make background jobs retryable and idempotent.
- Do not include Docker deployment in the MVP.

## 4. High-Level Architecture

```text
                         ┌──────────────┐
                         │    Client    │
                         └──────┬───────┘
                                │ HTTPS
                                ▼
                         ┌──────────────┐
                         │   FastAPI    │
                         │ API process  │
                         └──────┬───────┘
                                │
             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼
       Auth service       Document service     Query service
             │                  │                  │
             ▼                  ▼                  ▼
        User data       Job and file data    RAG orchestration
                                │                  │
                                ▼                  ▼
                         Background worker   Cache and retrieval
                                │                  │
                                ▼                  ▼
                         Ingestion pipeline   Hybrid search
                                                     │
                                                     ▼
                                                Re-ranker
                                                     │
                                                     ▼
                                                   LLM
```

## 5. Main Components

### API application

The API handles authentication, document management, queries, job status,
health checks, and metrics. It validates requests and delegates long-running
work to the worker.

### Background worker

The worker processes uploaded documents outside the request-response path. It
parses files, creates chunks, generates embeddings, and updates indexes.

### Relational database

The database stores users, documents, jobs, chunks, permissions, and query
metadata. A vector extension is used for semantic search, while full-text
search supports exact keyword matches.

### File storage

The original uploaded files are stored separately from searchable chunks. The
MVP uses local file storage under `data/uploads/`.

### Retrieval pipeline

The query service performs permission filtering, vector search, keyword
search, result merging, duplicate removal, and re-ranking.

### Generation pipeline

The generation service builds a bounded context with source metadata and sends
it to the LLM using a grounding prompt. The response is returned with
citations.

## 6. Document Ingestion Flow

```text
Client upload
    → Validate extension, size, and ownership
    → Save original file
    → Create document and job records
    → Return job_id
    → Worker claims job
    → Parse and clean text
    → Chunk text with metadata
    → Generate embeddings in batches
    → Index vectors and keywords
    → Mark job and document completed
```

The worker records failure details and may retry transient errors. A file
hash and document version prevent duplicate indexing.

## 7. Question Flow

```text
Client question
    → Authenticate request
    → Resolve accessible documents
    → Check query cache
    → Create query embedding
    → Vector search and keyword search
    → Merge using rank fusion
    → Re-rank candidates
    → Build context and citations
    → Generate grounded answer
    → Record metrics and return response
```

The system returns an explicit insufficient-context response when no reliable
source can support an answer.

## 8. Data Ownership and Security

Every document has an owner. Optional permission records allow sharing with
other users. Permission filters are applied in the database query and are
checked again before context construction. The LLM never receives chunks
outside the requesting user's access scope.

## 9. Reliability Design

- API requests use timeouts for external model calls.
- Safe transient operations use bounded exponential retries.
- Job processing is idempotent.
- Job status changes are persisted.
- A failed job does not expose partial content as completed content.
- Health endpoints distinguish application health from dependency health.

## 10. Performance Design

The system records latency for authentication, embedding, vector search,
keyword search, re-ranking, context construction, and generation. Vector and
keyword searches may run concurrently. Embeddings are batched, repeated
queries are cached, and only a bounded number of chunks are sent to the LLM.

## 11. Initial Capacity Assumptions

The MVP is designed for local development and small team usage. Capacity will
be established through load testing rather than assumed. The design can later
separate the worker, search service, and API horizontally if measurements
show that the modular monolith is insufficient.

## 12. Design Trade-offs

| Decision | Benefit | Trade-off |
|---|---|---|
| Modular monolith | Simple to develop and debug | Less independent scaling |
| Hybrid search | Better exact-term and semantic retrieval | More query work |
| Background worker | Responsive uploads | Requires job monitoring |
| Local file storage | Easy local setup | Not ideal for multi-machine deployment |
| Re-ranking | Better top results | Adds latency and model cost |
