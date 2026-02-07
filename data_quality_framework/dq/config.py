import os
from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://dq:dq@localhost:5432/dq")
    KAFKA_BOOTSTRAP: str = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
    RULES_PATH: str = os.getenv("RULES_PATH", "config/rules.yaml")

settings = Settings()
