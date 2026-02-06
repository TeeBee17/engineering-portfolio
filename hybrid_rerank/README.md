# Project 3: Hybrid Retrieval + Reranking (BM25 + Vector + Feature Reranker)

This demo implements:
- BM25 lexical retrieval (rank-bm25)
- Vector retrieval (FAISS cosine)
- Hybrid fusion (weighted sum of normalized scores)
- Lightweight reranking (feature-based: overlap + phrase hits)

## Run locally
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m app.seed
uvicorn app.api:app --reload

## Example query
curl -s -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"reset MFA for admin", "top_k":5, "use_rerank":true}'

## Tests
pytest -q


## Use Case
Hybrid Retrieval + Reranking (Better Relevance + Low Latency)
Real-life use case

Users ask messy queries like:

“reset MFA for admin”

“login loop after SSO”

“customer can’t access portal”

A pure vector search often returns close-but-wrong results.
A pure keyword search misses semantic matches.

Hybrid + reranking gives the best of both.

Why it matters

Increases answer quality for RAG

Reduces hallucinations (because retrieval improves)

Keeps latency fast enough for real-time agent workflows