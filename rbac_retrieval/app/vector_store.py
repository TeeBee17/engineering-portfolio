from typing import Dict, List, Tuple
import numpy as np
import faiss
from app.config import settings

class VectorStore:
    """
    Multi-tenant FAISS store.

    Uses IVF index with IDSelector filtering to enforce permission-first retrieval:
    we only score among allowed IDs (post-policy).
    """

    def __init__(self, dim: int = settings.VECTOR_DIM, nlist: int = settings.FAISS_NLIST, nprobe: int = settings.FAISS_NPROBE):
        self.dim = dim
        self.nlist = nlist
        self.nprobe = nprobe
        self._tenant_indexes: Dict[str, faiss.Index] = {}
        self._tenant_trained: Dict[str, bool] = {}

    def _make_ivf_index(self) -> faiss.IndexIVFFlat:
        # Cosine similarity via normalized vectors + inner product
        quantizer = faiss.IndexFlatIP(self.dim)
        index = faiss.IndexIVFFlat(quantizer, self.dim, self.nlist, faiss.METRIC_INNER_PRODUCT)
        index.nprobe = self.nprobe
        return index

    def upsert(self, tenant_id: str, ids: List[int], vectors: np.ndarray) -> None:
        if tenant_id not in self._tenant_indexes:
            self._tenant_indexes[tenant_id] = self._make_ivf_index()
            self._tenant_trained[tenant_id] = False

        index = self._tenant_indexes[tenant_id]

        vecs = vectors.astype("float32")
        faiss.normalize_L2(vecs)

        # Train once per tenant if IVF
        if isinstance(index, faiss.IndexIVFFlat) and not self._tenant_trained[tenant_id]:
            if vecs.shape[0] < max(50, self.nlist):
                # Not enough vectors to train IVF well -> fall back to flat
                flat = faiss.IndexFlatIP(self.dim)
                flat.add_with_ids(vecs, np.array(ids, dtype=np.int64))
                self._tenant_indexes[tenant_id] = flat
                self._tenant_trained[tenant_id] = True
                return

            index.train(vecs)
            self._tenant_trained[tenant_id] = True

        # Add vectors with ids
        index.add_with_ids(vecs, np.array(ids, dtype=np.int64))

    def search_with_allowed_ids(
        self,
        tenant_id: str,
        query_vec: np.ndarray,
        allowed_ids: List[int],
        top_k: int,
        oversample: int = 50
    ) -> List[Tuple[int, float]]:
        if tenant_id not in self._tenant_indexes:
            return []

        index = self._tenant_indexes[tenant_id]

        q = query_vec.astype("float32").reshape(1, -1)
        faiss.normalize_L2(q)

        if not allowed_ids:
            return []

        selector = faiss.IDSelectorBatch(np.array(allowed_ids, dtype=np.int64))
        k = min(top_k + oversample, 1000)

        # Permission-first search: IDSelector applied inside FAISS
        try:
            if isinstance(index, faiss.IndexIVFFlat):
                params = faiss.SearchParametersIVF()
                params.sel = selector
                D, I = index.search(q, k, params)
            else:
                # Flat index doesn't support IVF params; filter via IDSelector isn't exposed.
                # Fallback: search then filter (still tenant-safe, but not as strict as true pre-filter).
                D, I = index.search(q, k)
        except Exception:
            D, I = index.search(q, k)

        hits: List[Tuple[int, float]] = []
        for doc_id, score in zip(I[0].tolist(), D[0].tolist()):
            if doc_id == -1:
                continue
            # If flat fallback, enforce allowed_ids here
            if doc_id not in set(allowed_ids):
                continue
            hits.append((int(doc_id), float(score)))

        hits.sort(key=lambda x: x[1], reverse=True)
        return hits[:top_k]
