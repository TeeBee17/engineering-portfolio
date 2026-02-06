import numpy as np
from app.metadata_store import MetadataStore
from app.vector_store import VectorStore
from app.retrieval import toy_embed
from app.config import settings

def main():
    ms = MetadataStore()
    vs = VectorStore(dim=settings.VECTOR_DIM)

    tenantA = "tenantA"
    docsA = [
        (1, "Reset password steps", "kb", "KB-100", "public", ["cs_agent"], []),
        (2, "VIP account escalation playbook", "kb", "KB-200", "restricted", ["admin"], ["user1"]),
        (3, "CASE-123: customer cannot login", "case", "CASE-123", "internal", ["cs_agent"], []),
    ]

    tenantB = "tenantB"
    docsB = [
        (10, "TenantB password reset", "kb", "KB-555", "public", ["cs_agent"], []),
        (11, "TenantB sensitive runbook", "kb", "KB-777", "restricted", ["admin"], []),
    ]

    for doc_id, title, obj_type, obj_id, vis, roles, users in docsA:
        ms.upsert_doc(tenantA, doc_id, title, obj_type, obj_id, vis, roles, users)
    for doc_id, title, obj_type, obj_id, vis, roles, users in docsB:
        ms.upsert_doc(tenantB, doc_id, title, obj_type, obj_id, vis, roles, users)

    for tenant, docs in [(tenantA, docsA), (tenantB, docsB)]:
        ids = [d[0] for d in docs]
        vecs = np.vstack([toy_embed(d[1], settings.VECTOR_DIM) for d in docs]).astype("float32")
        vs.upsert(tenant, ids, vecs)

    # Patch the running app module (useful for tests / single-process runs)
    from app import main as app_main
    app_main.metadata = ms
    app_main.vectors = vs
    app_main.retrieval = RetrievalService(ms, vs)  # type: ignore[name-defined]

    print("Seed complete. Now run: uvicorn app.main:app --reload")

if __name__ == "__main__":
    # Local run: python -m app.seed
    from app.retrieval import RetrievalService
    main()
