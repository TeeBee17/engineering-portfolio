from typing import Dict, Optional
import numpy as np

from app.auth import Principal
from app.metadata_store import MetadataStore
from app.policy import PolicyEngine
from app.vector_store import VectorStore
from app.audit import audit_log

def toy_embed(text: str, dim: int) -> np.ndarray:
    """
    Deterministic pseudo-embedding from hashing (demo only).
    Replace with real embeddings in production.
    """
    rng = np.random.default_rng(abs(hash(text)) % (2**32))
    v = rng.normal(size=(dim,)).astype("float32")
    return v

class RetrievalService:
    def __init__(self, metadata: MetadataStore, vectors: VectorStore):
        self.metadata = metadata
        self.vectors = vectors

    def search(self, principal: Principal, query: str, top_k: int, request_filters: Optional[Dict[str, str]] = None):
        acl_map = self.metadata.load_acl_map()
        policy = PolicyEngine(acl_map)

        tenant_doc_ids = self.metadata.bulk_list_doc_ids(principal.tenant_id)
        decision = policy.authorize_docs(principal, tenant_doc_ids, request_filters=request_filters)
        allowed_ids = sorted(list(decision.allowed_doc_ids))

        qvec = toy_embed(query, self.vectors.dim)

        hits = self.vectors.search_with_allowed_ids(
            tenant_id=principal.tenant_id,
            query_vec=qvec,
            allowed_ids=allowed_ids,
            top_k=top_k
        )

        out = []
        for doc_id, score in hits:
            doc = self.metadata.get_doc(principal.tenant_id, doc_id)
            if not doc:
                continue
            out.append({
                "doc_id": doc_id,
                "score": score,
                "title": doc["title"],
                "object_type": doc["object_type"],
                "object_id": doc["object_id"],
            })

        audit_log(
            tenant_id=principal.tenant_id,
            user_id=principal.user_id,
            role=principal.role,
            action="search",
            detail={
                "query": query,
                "top_k": top_k,
                "filters": request_filters or {},
                "allowed_set_size": len(allowed_ids),
                "returned": len(out),
                "policy_reason": decision.reason,
            }
        )

        return out
