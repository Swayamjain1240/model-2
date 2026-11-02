# RFC-001: Hybrid Retrieval and Re-ranking

## 1. RFC Information

| Field | Value |
|---|---|
| Status | Proposed |
| Author | Model 2 project team |
| Date | 2026-11-02 |
| Reviewers | Project developers and reviewers |

## 2. Summary

This RFC proposes combining semantic vector search and keyword search, then
using a re-ranking stage before context is sent to the LLM.

## 3. Problem

Vector search understands related meaning but may miss exact technical terms,
identifiers, error codes, or API names. Keyword search handles exact matches
but may fail when the user uses different wording. A single retrieval method
therefore creates avoidable recall and precision problems.

## 4. Proposal

For each authorized query:

```text
Question
  → Query embedding
  → Vector top 20
  → Keyword top 20
  → Rank fusion and deduplication
  → Re-rank candidates
  → Select top 5–8 context chunks
```

Permission filters are applied to both searches before results are merged.

## 5. Alternatives Considered

### Vector search only

Simple and useful for the first prototype, but weak for exact terms.

### Keyword search only

Easy to inspect, but weak when users use synonyms or different phrasing.

### Hybrid search without re-ranking

Improves recall but may send noisy chunks to the LLM.

### Hybrid search with re-ranking

Adds latency and model cost but provides a better final context set. This is
the recommended approach for the engineering MVP.

## 6. Configuration

Initial configuration should be explicit and measurable:

```text
VECTOR_TOP_K=20
KEYWORD_TOP_K=20
RERANK_TOP_K=20
CONTEXT_TOP_K=6
```

These values are starting points, not guaranteed optimal values. Evaluation
will determine the best settings.

## 7. Evaluation Plan

Compare these configurations on the same golden dataset:

1. Vector search only.
2. Keyword search only.
3. Hybrid search without re-ranking.
4. Hybrid search with re-ranking.

Compare Recall@5, MRR, faithfulness, answer correctness, p95 latency, and
cost per query.

## 8. Risks

| Risk | Mitigation |
|---|---|
| Additional latency | Parallel search, caching, and bounded candidates |
| Model cost | Use a small re-ranker and measure token/provider cost |
| Score incompatibility | Use rank fusion instead of directly adding raw scores |
| Permission leakage | Apply access filters before both searches |
| Noisy context | Deduplicate and re-rank before generation |

## 9. Rollout Plan

1. Implement vector and keyword adapters.
2. Add rank fusion behind a configuration flag.
3. Add re-ranking behind a second flag.
4. Run offline evaluation.
5. Run load tests.
6. Make the best measured configuration the default.

## 10. Open Questions

- Which embedding model gives the best quality and cost for the target files?
- Which re-ranking model is fast enough for the local environment?
- Should keyword search use PostgreSQL full-text search or a dedicated index?
