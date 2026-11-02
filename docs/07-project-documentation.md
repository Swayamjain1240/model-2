# Project Documentation

## 1. Project Overview

Model 2 is an engineering-focused RAG system that allows users to upload
documents and ask questions about their content. It combines document
ingestion, semantic retrieval, keyword search, re-ranking, and grounded answer
generation.

## 2. Project Goals

- Build a reliable document question-answering MVP.
- Learn practical system design and backend engineering.
- Measure retrieval quality instead of relying only on visual responses.
- Measure latency, throughput, cost, and reliability.
- Create an upgrade path toward a production-ready system.

## 3. Repository Structure

```text
model 2/
├── app/             # Application source code
├── docs/            # Design and project documentation
├── tests/           # Unit, integration, and end-to-end tests
├── evaluations/     # Golden questions and quality reports
├── load_tests/      # Load-test scenarios
├── scripts/         # Local setup and maintenance scripts
├── data/uploads/    # Local original documents; do not commit user data
├── README.md
└── .env.example
```

## 4. Development Workflow

1. Read or update the relevant design document.
2. Create a focused implementation change.
3. Add or update tests.
4. Run formatting, tests, and relevant evaluation checks.
5. Review logs and metrics for the changed workflow.
6. Commit one logical change with a conventional commit message.

## 5. Development Milestones

### Milestone 1: Basic RAG

Implement upload, parsing, chunking, embeddings, retrieval, answer
generation, and citations.

### Milestone 2: Async ingestion

Add job records, worker processing, status endpoints, retries, and duplicate
detection.

### Milestone 3: Retrieval quality

Add keyword search, hybrid ranking, metadata filters, and re-ranking.

### Milestone 4: Security

Add authentication, document ownership, sharing, and permission-aware search.

### Milestone 5: Engineering measurement

Add evaluation, caching, monitoring, tracing, and load testing.

## 6. Local Operations

The API and worker run as separate local processes. Database and model-provider
configuration is supplied through environment variables. Docker is not part of
the current project workflow.

Operational checks include:

- API health check
- Database connectivity
- Worker job status
- Failed-job review
- Storage capacity
- Model-provider availability

## 7. Documentation Rules

- Keep requirements separate from implementation details.
- Record important design changes in an RFC or decision record.
- Use diagrams and examples where they improve understanding.
- Update documentation when an interface or workflow changes.
- Never commit passwords, tokens, private documents, or generated secrets.

## 8. Glossary

| Term | Meaning |
|---|---|
| RAG | Retrieval-Augmented Generation |
| Chunk | Searchable portion of a document |
| Embedding | Numeric representation of text meaning |
| Re-ranker | Model or algorithm that reorders candidates |
| Recall@K | Whether a relevant result appears in the first K results |
| Faithfulness | Whether an answer is supported by retrieved context |
| p95 latency | Time within which 95% of requests complete |
