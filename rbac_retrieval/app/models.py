from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(10, ge=1, le=50)
    filters: Optional[Dict[str, str]] = None  # e.g., {"object_type":"case"}

class SearchHit(BaseModel):
    doc_id: int
    score: float
    title: str
    object_type: str
    object_id: str

class SearchResponse(BaseModel):
    tenant_id: str
    user_id: str
    role: str
    hits: List[SearchHit]
