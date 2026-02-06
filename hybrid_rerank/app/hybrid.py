from typing import Dict, List, Tuple
from app.config import settings

def _minmax_norm(scores: Dict[int, float]) -> Dict[int, float]:
    if not scores:
        return {}
    vals = list(scores.values())
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-9:
        return {k: 1.0 for k in scores}
    return {k: (v - lo) / (hi - lo) for k, v in scores.items()}

def fuse(
    bm25_hits: List[Tuple[int, float]],
    vec_hits: List[Tuple[int, float]],
    w_bm25: float = settings.W_BM25,
    w_vec: float = settings.W_VEC,
    max_candidates: int = settings.HYBRID_CANDIDATES
) -> Dict[int, Dict[str, float]]:
    """Returns {doc_id: {bm25_score, vec_score, hybrid_score}}."""
    bm = {doc_id: score for doc_id, score in bm25_hits}
    vx = {doc_id: score for doc_id, score in vec_hits}

    bm_n = _minmax_norm(bm)
    vx_n = _minmax_norm(vx)

    candidates = set(list(bm.keys()) + list(vx.keys()))

    combined: Dict[int, Dict[str, float]] = {}
    for doc_id in candidates:
        b = bm_n.get(doc_id, 0.0)
        v = vx_n.get(doc_id, 0.0)
        hybrid = w_bm25 * b + w_vec * v
        combined[doc_id] = {
            "bm25_score": float(bm.get(doc_id, 0.0)),
            "vec_score": float(vx.get(doc_id, 0.0)),
            "hybrid_score": float(hybrid),
        }

    top = sorted(combined.items(), key=lambda kv: kv[1]["hybrid_score"], reverse=True)[:max_candidates]
    return dict(top)
