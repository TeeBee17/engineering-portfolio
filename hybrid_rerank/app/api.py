from fastapi import FastAPI
from app.models import SearchRequest, SearchResponse, SearchHit
from app.store import InMemoryDocStore
from app.lexical import BM25Index
from app.vector import FaissVectorIndex
from app.hybrid import fuse
from app.rerank import rerank

app = FastAPI(title="Hybrid Retrieval + Reranking Demo")

store = InMemoryDocStore()
bm25 = BM25Index()
vec = FaissVectorIndex()

def rebuild_indexes():
    docs = store.all_docs()
    bm25.build(docs)
    vec.build(docs)

@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    filter_object_type = (req.filters or {}).get("object_type")

    docs_by_id = store.docs_by_id
    bm25_hits = bm25.search(req.query, k=50, filter_object_type=filter_object_type, docs_by_id=docs_by_id)
    vec_hits = vec.search(req.query, k=50, filter_object_type=filter_object_type, docs_by_id=docs_by_id)

    fused = fuse(bm25_hits, vec_hits)

    if req.use_rerank:
        ranked = rerank(req.query, fused, docs_by_id)
        final_order = ranked[:req.top_k]
        final_scores = {doc_id: score for doc_id, score in final_order}
    else:
        order = sorted(fused.items(), key=lambda kv: kv[1]["hybrid_score"], reverse=True)[:req.top_k]
        final_scores = {doc_id: float(scores["hybrid_score"]) for doc_id, scores in order}

    hits = []
    for doc_id, final_score in sorted(final_scores.items(), key=lambda x: x[1], reverse=True):
        d = docs_by_id[doc_id]
        s = fused[doc_id]
        hits.append(SearchHit(
            doc_id=doc_id,
            title=d.title,
            object_type=d.object_type,
            object_id=d.object_id,
            bm25_score=float(s["bm25_score"]),
            vec_score=float(s["vec_score"]),
            hybrid_score=float(s["hybrid_score"]),
            final_score=float(final_score),
        ))

    return SearchResponse(hits=hits)
