# Software Design Document

## 1. Document Information

| Field | Value |
|---|---|
| Project | Engineering-Focused Document RAG System |
| Version | 1.0 |
| Status | Draft |
| Audience | Software engineers |

## 2. Purpose

This document defines the internal software structure of the RAG application.
The goal is to keep the code understandable for a junior developer while
maintaining clear boundaries for future upgrades.

## 3. Module Structure

```text
API routes
    ↓
Application services
    ↓
Domain workflows
    ↓
Repositories and provider interfaces
    ↓
Database, file system, cache, and external models
```

## 4. Module Responsibilities

### API layer

Responsible for HTTP routing, request validation, authentication dependencies,
response serialization, and status codes. It must not contain chunking,
retrieval, or LLM orchestration logic.

### Service layer

Coordinates use cases such as upload document, process job, answer question,
share document, and delete document.

### Ingestion module

Contains parser adapters, text cleaning, chunking, metadata extraction, and
the ingestion pipeline.

### Retrieval module

Contains embedding generation, vector search, keyword search, hybrid result
merging, filtering, and re-ranking.

### Generation module

Builds context, formats prompts, calls the LLM, validates the response, and
builds citations.

### Repository module

Owns persistence operations. Services use repositories instead of writing SQL
directly inside API route handlers.

### Worker module

Claims pending jobs, calls the ingestion service, records status changes, and
handles retry policy.

## 5. Provider Interfaces

External dependencies should be hidden behind small interfaces:

```text
DocumentParser.parse(file) -> ParsedDocument
Embedder.embed(texts) -> EmbeddingBatch
VectorIndex.search(vector, filters, limit) -> SearchResults
KeywordIndex.search(query, filters, limit) -> SearchResults
Reranker.rank(query, candidates) -> RankedResults
LLMClient.generate(messages) -> ModelResponse
Cache.get(key) / Cache.set(key, value, ttl)
```

This allows a test double or a different provider to be used without changing
the application services.

## 6. Core Use Cases

### Upload document

1. Authenticate the user.
2. Validate file metadata.
3. Calculate a content hash.
4. Store the original file.
5. Create a document record.
6. Create an ingestion job.
7. Return the document and job identifiers.

### Process document

1. Claim the job using a safe state transition.
2. Select the parser by file type.
3. Extract and clean text.
4. Create deterministic chunks.
5. Generate embeddings in batches.
6. Persist chunks and search indexes.
7. Mark the document as completed.

### Answer question

1. Authenticate the user.
2. Resolve accessible document IDs.
3. Check the cache.
4. Execute vector and keyword searches.
5. Merge and re-rank results.
6. Build bounded context with citations.
7. Call the LLM.
8. Return answer, citations, and timing information.

## 7. Error Handling

Errors are divided into four categories:

| Category | Example | Behavior |
|---|---|---|
| Validation | Unsupported file type | Return a clear 4xx response |
| Authorization | No document access | Return 403 or a safe not-found response |
| Dependency | Model timeout | Retry when safe, then return controlled failure |
| Internal | Unexpected exception | Log with request ID and return generic 500 |

Error responses must not expose secrets, stack traces, or document content.

## 8. State Machines

### Document state

```text
UPLOADED → PROCESSING → COMPLETED
                    └→ FAILED → PROCESSING
```

### Job state

```text
PENDING → RUNNING → SUCCEEDED
                 └→ RETRYING → RUNNING
                 └→ FAILED
```

Only valid state transitions may be applied.

## 9. Testing Strategy

- Unit tests cover chunking, ranking, permission checks, and citation logic.
- Integration tests cover database repositories and search adapters.
- End-to-end tests cover upload-to-answer behavior.
- Evaluation tests measure retrieval and answer quality.
- Load tests measure latency, throughput, and error behavior.

## 10. Configuration

Configuration comes from environment variables and is loaded through one
settings module. Secrets must never be committed. `.env.example` documents
required variable names without real credentials.
