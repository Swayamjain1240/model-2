# Problem Statement

## 1. Document Information

| Field | Value |
|---|---|
| Project | Engineering-Focused Document RAG System |
| Document | Problem Statement |
| Version | 1.0 |
| Status | Draft |
| Audience | Developers, reviewers, and project stakeholders |

## 2. Background

Teams store important information in PDFs, Markdown files, Word documents,
technical guides, API documentation, and internal knowledge bases. Finding
relevant information in these documents manually is slow and often requires
the user to search through several files before finding the correct answer.

The project will provide a document question-answering system based on
Retrieval-Augmented Generation (RAG). Users will upload documents and ask
questions in natural language. The system will retrieve relevant content from
the uploaded documents and use a language model to generate an answer with
source citations.

The system will not train a new language model. Instead, it will combine
document processing, search, retrieval, ranking, and language-model
generation into one measurable software system.

## 3. Problem Definition

Users need a reliable way to find answers from their own documents without
reading every document manually. A basic keyword search is not sufficient
because users may ask questions using words that do not exactly match the
source documents. A language model alone is also not sufficient because it
may generate unsupported or incorrect information.

The system must therefore:

1. Accept and process supported documents.
2. Convert document content into searchable chunks.
3. Retrieve relevant content using semantic and keyword search.
4. Respect document ownership and access permissions.
5. Generate answers based only on retrieved context.
6. Provide citations that identify the source of the answer.
7. Clearly indicate when the available documents do not contain enough
   information.
8. Provide measurable performance, quality, and reliability metrics.

## 4. Current Challenges

The system must address the following challenges:

### 4.1 Document processing

Documents have different formats and structures. Text may contain headings,
tables, page boundaries, code blocks, or formatting that must be preserved as
much as possible.

### 4.2 Retrieval quality

Semantic search is useful for understanding meaning, while keyword search is
important for exact terms such as error codes, API names, product names, and
identifiers. Using only one search method can result in missed information.

### 4.3 Answer reliability

The language model may hallucinate information if it receives incomplete or
irrelevant context. Answers must be grounded in retrieved document content.

### 4.4 Access control

Users must not be able to retrieve information from documents they do not own
or have permission to access.

### 4.5 Performance

Document ingestion and question answering may involve expensive operations,
including parsing, embedding generation, retrieval, re-ranking, and language
model generation. The system must measure and improve latency, throughput,
and resource usage.

### 4.6 Evaluation

RAG quality cannot be judged only by whether the API returns a response. The
system needs a test dataset and measurable retrieval and answer-quality
metrics.

## 5. Proposed Solution

Build a modular RAG application with two main workflows:

### Document ingestion workflow

```text
Upload document
    → Validate file
    → Store original document
    → Create background job
    → Parse text
    → Clean text
    → Create chunks
    → Generate embeddings
    → Store chunks and search indexes
    → Mark document as completed
```

### Question-answering workflow

```text
Ask question
    → Authenticate user
    → Check document permissions
    → Check cache
    → Run vector search
    → Run keyword search
    → Merge search results
    → Re-rank candidates
    → Build grounded context
    → Generate answer
    → Add citations
    → Record metrics
```

The first implementation will be a modular monolith with a FastAPI backend
and a separate background worker. Docker deployment is intentionally outside
the scope of this MVP.

## 6. Project Objectives

The project objectives are to:

- Build a working document-based RAG application.
- Support asynchronous document processing.
- Improve retrieval using hybrid search and re-ranking.
- Return grounded answers with source citations.
- Implement authentication and document-level permissions.
- Measure Recall@K, Precision@K, MRR, faithfulness, and citation accuracy.
- Measure p50 and p95 latency, throughput, error rate, and cache hit rate.
- Add structured logging, monitoring, and request tracing.
- Use load testing to understand system limits.
- Keep the design simple enough to run locally without Docker.

## 7. In Scope

The MVP includes:

- User registration and login.
- Document upload and document status tracking.
- Support for selected document formats such as PDF and Markdown.
- Text parsing and cleaning.
- Configurable text chunking.
- Embedding generation.
- Vector storage and retrieval.
- Keyword search.
- Hybrid retrieval.
- Result re-ranking.
- Answer generation using an LLM.
- Source citations.
- Document ownership and access permissions.
- Background ingestion jobs with retry handling.
- Caching for repeated queries and embeddings.
- Application logs, metrics, and tracing.
- Offline evaluation using a question-and-answer dataset.
- Load testing and latency measurement.

## 8. Out of Scope

The following items are not part of the initial MVP:

- Training a new foundation model.
- Fine-tuning a language model.
- Docker or Kubernetes deployment.
- A complex microservices architecture.
- Real-time collaborative document editing.
- Automatic correction of source documents.
- Guaranteed correctness for information missing from the uploaded files.
- Automatic ingestion from every possible file format.
- Production cloud deployment.

## 9. Users and Use Cases

### 9.1 Document owner

The document owner can upload documents, monitor processing status, ask
questions, and delete documents.

### 9.2 Authorized user

An authorized user can ask questions about documents shared with them and
receive answers with citations.

### 9.3 Developer or administrator

The developer or administrator can inspect job failures, review metrics,
run evaluations, and analyze latency and throughput.

## 10. Functional Requirements

### FR-01: User authentication

The system shall allow users to register, log in, and access protected APIs.

### FR-02: Document upload

The system shall validate and store supported documents uploaded by an
authenticated user.

### FR-03: Asynchronous processing

The system shall process uploaded documents in a background worker and return
a job identifier to the user.

### FR-04: Document indexing

The system shall parse, chunk, embed, and index document content.

### FR-05: Permission enforcement

The system shall restrict document search and retrieval to documents the user
is authorized to access.

### FR-06: Hybrid retrieval

The system shall combine semantic vector search and keyword search before
ranking the final results.

### FR-07: Re-ranking

The system shall re-rank candidate chunks and select the most relevant context
for answer generation.

### FR-08: Grounded answer generation

The system shall generate answers using retrieved document context and shall
avoid presenting unsupported information as fact.

### FR-09: Citations

The system shall return source information such as document name, page
number, section, or chunk identifier when available.

### FR-10: Evaluation and monitoring

The system shall record the information required to evaluate retrieval
quality, answer quality, latency, errors, token usage, and cache behavior.

## 11. Non-Functional Requirements

### Performance

- Record p50, p95, and p99 request latency.
- Record ingestion processing time.
- Support concurrent query requests during load testing.
- Use batching, caching, and concurrent retrieval where appropriate.

### Reliability

- Failed ingestion jobs shall be visible to the user or administrator.
- Safe operations shall support retries.
- Reprocessing the same document shall not create duplicate indexed content.
- External model calls shall have timeouts and controlled retries.

### Security

- Protected endpoints shall require authentication.
- Document permissions shall be checked before retrieval.
- Uploaded files shall be validated for type and size.
- Secrets shall be stored in environment variables, not source code.
- Sensitive document text shall not be written to normal application logs.

### Maintainability

- The application shall use clearly separated modules.
- Search, embedding, parsing, and LLM providers shall be replaceable.
- Important behavior shall have unit, integration, and end-to-end tests.
- Configuration shall be environment-based.

## 12. Success Criteria

The MVP will be considered successful when:

1. A user can upload a supported document and receive a completed ingestion
   status.
2. A user can ask a question and receive an answer based on the document.
3. The answer includes valid source citations.
4. Unauthorized users cannot retrieve protected document content.
5. The system can demonstrate hybrid retrieval and re-ranking.
6. A repeatable evaluation dataset produces retrieval and answer-quality
   reports.
7. The system reports p50 and p95 latency, throughput, and error rate.
8. Failed ingestion jobs can be retried safely.
9. Load testing produces a documented performance baseline.
10. The system can run locally without Docker.

## 13. Expected Deliverables

- Source code for the RAG application.
- Database schema and migration files.
- API documentation.
- Document ingestion worker.
- Retrieval and generation pipeline.
- Authentication and permission implementation.
- Evaluation dataset and evaluation report.
- Monitoring and tracing configuration.
- Load-test scripts and performance report.
- Project documentation describing architecture and implementation decisions.

## 14. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Poor chunking | Low retrieval quality | Compare chunking strategies using evaluation data |
| Irrelevant search results | Incorrect answers | Use hybrid search and re-ranking |
| LLM hallucination | Unreliable answers | Use strict grounding rules and citations |
| Slow model calls | High user latency | Cache, stream responses, use timeouts, measure each stage |
| Duplicate ingestion | Wasted storage and cost | Use file hashes and idempotent jobs |
| Unauthorized retrieval | Data exposure | Apply permissions during search and context construction |
| External provider failure | Failed requests | Add retries, timeouts, and clear error responses |
| Insufficient evaluation data | Misleading quality results | Build and maintain a representative question set |

## 15. Definition of Done

The problem statement is considered implemented when the project has a
working, locally runnable RAG MVP that satisfies the functional requirements,
records engineering metrics, passes its automated tests, and has documented
evaluation and load-test results.
