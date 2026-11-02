# Model 2: Engineering-Focused RAG System

An engineering-focused Retrieval-Augmented Generation (RAG) system for
uploading documents, retrieving relevant information, and generating answers
with source citations.

The project is being developed in stages. The first stage is an MVP that
focuses on a reliable document-to-answer workflow and measurable engineering
quality.

## MVP Workflow

```text
Upload document
    → Parse text
    → Create chunks
    → Generate embeddings
    → Store vectors
    → Ask questions
    → Retrieve context
    → Generate answer with citations
```

## Engineering Goals

The MVP will also include:

- Asynchronous document processing
- Hybrid vector and keyword search
- Result re-ranking
- Evaluation metrics such as Recall@K, Precision@K, and MRR
- Query and embedding caching
- Authentication and document-level permissions
- Monitoring and request tracing
- Latency and throughput measurement
- Load testing

Docker deployment is intentionally not part of the current MVP.

## Planned Architecture

The project will use a modular monolith with:

- FastAPI for the application API
- A background worker for document ingestion
- A relational database for users, documents, jobs, and metadata
- Vector search for semantic retrieval
- Keyword search for exact terms and identifiers
- A re-ranking stage before answer generation
- An LLM for grounded answer generation

The system will be designed to answer only from authorized, retrieved
document context and will return citations for important claims.

## Documentation

- [Problem Statement](docs/01-problem-statement.md)
- [System Design](docs/02-system-design.md)
- [Software Design](docs/03-software-design.md)
- [Technical Design](docs/04-technical-design.md)
- [Software Requirements](docs/05-software-requirements.md)
- [Architecture](docs/06-architecture.md)
- [Project Documentation](docs/07-project-documentation.md)
- [Engineering Design](docs/08-engineering-design.md)
- [RFC: Hybrid Retrieval and Re-ranking](docs/09-rfc-hybrid-retrieval.md)
- [Solution Design](docs/10-solution-design.md)

Additional design and implementation documents will be added as the project grows.

## Project Status

**Current stage:** Planning and MVP documentation

The implementation will be developed incrementally, beginning with the basic
RAG pipeline and then adding production-oriented engineering capabilities.

## Repository Structure

```text
.
├── docs/       # Project and engineering documentation
├── README.md   # Project overview
└── ...         # Application source and tests added during implementation
```
