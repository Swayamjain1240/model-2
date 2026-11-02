# Engineering Design Document

## 1. Document Information

| Field | Value |
|---|---|
| Project | Engineering-Focused Document RAG System |
| Version | 1.0 |
| Status | Draft |
| Audience | Engineers responsible for quality and operations |

## 2. Purpose

This document defines how the project will measure and improve production-
oriented qualities: correctness, retrieval quality, latency, throughput,
reliability, security, and operability.

## 3. Quality Model

```text
Correctness  = relevant retrieval + grounded generation
Performance  = bounded latency + acceptable throughput
Reliability  = safe retries + clear failures + idempotent jobs
Security     = authenticated and permission-aware access
Operability  = logs + metrics + traces + runbooks
```

## 4. Retrieval Evaluation

Maintain a versioned dataset containing questions, expected answers, relevant
documents, and relevant chunk IDs.

Track:

- Recall@K
- Precision@K
- Mean Reciprocal Rank (MRR)
- nDCG when graded relevance is available
- Duplicate-result rate
- No-result rate

Each retrieval change must be evaluated against the same baseline dataset.

## 5. Answer Evaluation

Track:

- Answer correctness
- Faithfulness to retrieved context
- Citation accuracy
- Answer completeness
- Appropriate abstention when context is insufficient

Automated model-based evaluation may assist review, but a sample of results
should also be checked manually.

## 6. Performance Engineering

Measure each pipeline stage independently:

```text
Authentication
Query normalization
Embedding
Vector search
Keyword search
Result merging
Re-ranking
Context construction
LLM generation
Response serialization
```

Primary metrics are p50, p95, and p99 latency. Throughput is measured in
successful queries per second at a stated concurrency level.

Potential optimizations include batching embeddings, concurrent independent
searches, bounded context size, caching, connection pooling, and response
streaming.

## 7. Reliability Engineering

- Use timeouts for every external call.
- Retry only transient failures.
- Use exponential backoff with a maximum attempt count.
- Make ingestion idempotent using document hashes and versions.
- Persist job state before and after each major stage.
- Return safe error messages to users.
- Keep failed jobs available for inspection and retry.

## 8. Caching Strategy

Cache query embeddings and eligible final responses. Cache keys must include
the user access scope and document version. A permission check is always
performed before returning cached document-derived content. Cache invalidation
occurs when a document is deleted, replaced, or permission changes.

## 9. Security Engineering

- Hash passwords using a modern password-hashing algorithm.
- Use short-lived access tokens and secure secret configuration.
- Validate file type, extension, size, and content where possible.
- Prevent path traversal when saving uploads.
- Apply permission filters before retrieval and generation.
- Treat document text as untrusted input to reduce prompt-injection risk.
- Do not place secrets or sensitive document text in logs.

## 10. Observability

Use a correlation ID across the API request, database operations, worker job,
retrieval pipeline, and model calls. Publish counters, gauges, and latency
histograms. Logs should be structured and searchable.

Important dashboards include:

- Request rate and error rate
- p50/p95/p99 query latency
- Ingestion success and failure rate
- Queue depth and job age
- Cache hit rate
- Token usage and model cost
- Retrieval result counts

## 11. Load Testing

Load tests should include:

1. Concurrent query requests.
2. Repeated common questions to measure caching.
3. Upload and ingestion workloads.
4. Mixed upload and query traffic.
5. Failure behavior when the model provider is slow.

Each report must state dataset size, concurrency, duration, environment,
success rate, p50 latency, p95 latency, p99 latency, and throughput.

## 12. Testing Pyramid

```text
        End-to-end tests
      Integration tests
    Unit and contract tests
```

Unit tests should be numerous and fast. Integration tests verify databases and
search providers. End-to-end tests verify the complete user workflow.

## 13. Engineering Definition of Done

A feature is complete only when its implementation, tests, logs, metrics,
failure behavior, and documentation are updated. Performance-sensitive
features also require a benchmark or load-test comparison.
