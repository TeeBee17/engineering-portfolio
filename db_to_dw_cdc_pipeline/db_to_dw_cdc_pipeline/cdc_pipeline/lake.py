from __future__ import annotations
from typing import Dict, Any
import os, json
from datetime import datetime, timezone
import pyarrow as pa
import pyarrow.parquet as pq

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)

class ParquetLake:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def append_change(self, record: Dict[str, Any]) -> str:
        now = _utc_now()
        part = os.path.join(self.base_dir, f"date={now.strftime('%Y-%m-%d')}")
        os.makedirs(part, exist_ok=True)
        path = os.path.join(part, f"cdc_{now.strftime('%H%M%S_%f')}.parquet")

        row = {
            "ingested_at": now.isoformat(),
            "event_id": record.get("event_id"),
            "table": record.get("table"),
            "op": record.get("op"),
            "ts_ms": int(record.get("ts_ms") or 0),
            "pk_json": json.dumps(record.get("pk") or {}, sort_keys=True),
            "before_json": json.dumps(record.get("before") or {}, sort_keys=True),
            "after_json": json.dumps(record.get("after") or {}, sort_keys=True),
        }
        pq.write_table(pa.Table.from_pylist([row]), path)
        return path
