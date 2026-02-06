from fastapi import FastAPI, Header, HTTPException
from app.models import SearchRequest, SearchResponse, SearchHit
from app.auth import parse_bearer_token
from app.metadata_store import MetadataStore
from app.vector_store import VectorStore
from app.retrieval import RetrievalService

app = FastAPI(title="RBAC-safe Multi-tenant Retrieval")

metadata = MetadataStore()
vectors = VectorStore()
retrieval = RetrievalService(metadata, vectors)

@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest, authorization: str = Header(default="")):
    try:
        principal = parse_bearer_token(authorization)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    hits = retrieval.search(
        principal=principal,
        query=req.query,
        top_k=req.top_k,
        request_filters=req.filters
    )

    return SearchResponse(
        tenant_id=principal.tenant_id,
        user_id=principal.user_id,
        role=principal.role,
        hits=[SearchHit(**h) for h in hits]
    )
