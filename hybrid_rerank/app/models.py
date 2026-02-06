from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class Doc(BaseModel):
    doc_id: int
    title: str
    body: str
    object_type: str   # "case" | "kb" | "note"
    object_id: str

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(10, ge=1, le=50)
    filters: Optional[Dict[str, str]] = None   # e.g. {"object_type":"kb"}
    use_rerank: bool = True

class SearchHit(BaseModel):
    doc_id: int
    title: str
    object_type: str
    object_id: str
    bm25_score: float
    vec_score: float
    hybrid_score: float
    final_score: float

class SearchResponse(BaseModel):
    hits: List[SearchHit]
