from pydantic import BaseModel
import os

class Settings(BaseModel):
    DB_PATH: str = os.getenv("DB_PATH", "rbac_retrieval.sqlite3")
    VECTOR_DIM: int = int(os.getenv("VECTOR_DIM", "384"))
    FAISS_NLIST: int = int(os.getenv("FAISS_NLIST", "32"))  # IVF clusters
    FAISS_NPROBE: int = int(os.getenv("FAISS_NPROBE", "8"))  # search probes
    AUDIT_LOG_PATH: str = os.getenv("AUDIT_LOG_PATH", "audit.log")

settings = Settings()
