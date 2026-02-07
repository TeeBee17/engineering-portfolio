from __future__ import annotations
import os
from pydantic import BaseModel

class Settings(BaseModel):
    kafka_bootstrap: str = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
    topic: str = os.getenv("CDC_TOPIC", "dbserver1.public.customers")
    group: str = os.getenv("CDC_GROUP", "cdc-dw-consumer")

    duckdb_path: str = os.getenv("DUCKDB_PATH", "warehouse/warehouse.duckdb")
    lake_customers_dir: str = os.getenv("LAKE_CUSTOMERS_DIR", "warehouse/lake/customers")

settings = Settings()
