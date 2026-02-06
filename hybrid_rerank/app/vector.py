from typing import List, Tuple, Dict, Optional
import numpy as np
import faiss
from app.models import Doc
from app.config import settings

def toy_embed(text: str, dim: int) -> np.ndarray:
    """Deterministic toy embedding for a runnable demo."""
    rng = np.random.default_rng(abs(hash(text)) % (2**32))
    v = rng.normal(size=(dim,)).astype("float32")
    return v

class FaissVectorIndex:
    """Cosine similarity using normalized vectors + inner product."""
    def __init__(self, dim: int = settings.VECTOR_DIM):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.doc_ids: List[int] = []

    def build(self, docs: List[Doc]) -> None:
        self.doc_ids = [d.doc_id for d in docs]
        vecs = np.vstack([toy_embed(d.title + " " + d.body, self.dim) for d in docs]).astype("float32")
        faiss.normalize_L2(vecs)
        self.index.reset()
        self.index.add(vecs)

    def search(self, query: str, k: int, filter_object_type: Optional[str] = None, docs_by_id: Dict[int, Doc] = None) -> List[Tuple[int, float]]:
        if self.index.ntotal == 0:
            return []
        qv = toy_embed(query, self.dim).astype("float32").reshape(1, -1)
        faiss.normalize_L2(qv)

        D, I = self.index.search(qv, min(k * 5, len(self.doc_ids)))
        hits: List[Tuple[int, float]] = []
        for idx, score in zip(I[0].tolist(), D[0].tolist()):
            if idx < 0:
                continue
            doc_id = self.doc_ids[idx]
            if filter_object_type and docs_by_id:
                d = docs_by_id.get(doc_id)
                if not d or d.object_type != filter_object_type:
                    continue
            hits.append((doc_id, float(score)))
            if len(hits) >= k:
                break
        return hits
