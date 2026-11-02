# Software Requirements Specification

## 1. Document Information

| Field | Value |
|---|---|
| Project | Engineering-Focused Document RAG System |
| Version | 1.0 |
| Status | Draft |
| Audience | Developers, reviewers, and stakeholders |

## 2. Purpose

This document defines what the MVP must do and the quality constraints it
must satisfy. It is the baseline for implementation and acceptance testing.

## 3. Actors

| Actor | Responsibility |
|---|---|
| User | Uploads documents and asks questions |
| Document owner | Controls access to an uploaded document |
| Authorized user | Uses documents shared with them |
| Administrator/developer | Reviews jobs, metrics, and evaluations |
| External model provider | Creates embeddings and generated answers |

## 4. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | The system shall allow a user to register and log in. | Must |
| FR-002 | The system shall authenticate protected API requests. | Must |
| FR-003 | The system shall accept supported document formats. | Must |
| FR-004 | The system shall reject unsupported files and invalid sizes. | Must |
| FR-005 | The system shall store the original uploaded document. | Must |
| FR-006 | The system shall create an asynchronous ingestion job. | Must |
| FR-007 | The system shall expose ingestion status and failure information. | Must |
| FR-008 | The system shall parse, clean, and chunk document text. | Must |
| FR-009 | The system shall generate and store embeddings for chunks. | Must |
| FR-010 | The system shall support semantic vector retrieval. | Must |
| FR-011 | The system shall support keyword retrieval. | Must |
| FR-012 | The system shall combine vector and keyword results. | Must |
| FR-013 | The system shall re-rank candidate chunks. | Must |
| FR-014 | The system shall enforce document permissions during retrieval. | Must |
| FR-015 | The system shall generate answers from retrieved context. | Must |
| FR-016 | The system shall return citations for answer sources. | Must |
| FR-017 | The system shall indicate when context is insufficient. | Must |
| FR-018 | The system shall cache eligible repeated operations. | Should |
| FR-019 | The system shall record query and pipeline metrics. | Must |
| FR-020 | The system shall support document deletion and reprocessing. | Should |

## 5. Non-Functional Requirements

### NFR-001: Performance

The system shall record p50, p95, and p99 query latency and shall report
throughput and error rate during load testing.

### NFR-002: Reliability

Transient external failures shall use bounded retries and timeouts. Job
processing shall be idempotent and safe to retry.

### NFR-003: Security

Passwords shall be hashed, secrets shall be configuration-based, and users
shall not retrieve documents outside their permission scope.

### NFR-004: Maintainability

Parsing, embeddings, retrieval, ranking, and generation shall be replaceable
through clear module boundaries.

### NFR-005: Observability

Requests and jobs shall have correlation IDs, structured logs, timing data,
and error information that does not expose sensitive document content.

### NFR-006: Usability

The API shall return clear status values, validation errors, and citations.

### NFR-007: Portability

The MVP shall run locally without Docker and shall use environment-based
configuration for external dependencies.

## 6. Acceptance Criteria

The MVP passes acceptance when a test user can upload a supported document,
observe processing completion, ask a question, receive a grounded answer with
valid citations, and be denied access to another user's private document.

The evaluation suite must also produce retrieval metrics and the load-test
suite must produce a latency and throughput report.

## 7. Traceability

Requirements map to the following documents:

- System flow: `02-system-design.md`
- Internal modules: `03-software-design.md`
- Technical implementation: `04-technical-design.md`
- Architecture decisions: `06-architecture.md`
- Engineering quality: `08-engineering-design.md`
