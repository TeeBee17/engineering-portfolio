from pydantic import BaseModel
import os

class Settings(BaseModel):
    VECTOR_DIM: int = int(os.getenv("VECTOR_DIM", "384"))

    # Retrieval sizes
    BM25_K: int = int(os.getenv("BM25_K", "50"))
    VEC_K: int = int(os.getenv("VEC_K", "50"))
    HYBRID_CANDIDATES: int = int(os.getenv("HYBRID_CANDIDATES", "80"))

    # Fusion weights
    W_BM25: float = float(os.getenv("W_BM25", "0.55"))
    W_VEC: float = float(os.getenv("W_VEC", "0.45"))

    # Reranking weights (feature-based)
    RERANK_W_HYBRID: float = float(os.getenv("RERANK_W_HYBRID", "0.65"))
    RERANK_W_PHRASE: float = float(os.getenv("RERANK_W_PHRASE", "0.20"))
    RERANK_W_OVERLAP: float = float(os.getenv("RERANK_W_OVERLAP", "0.15"))

settings = Settings()
