from __future__ import annotations
from typing import Any, Dict, Optional
from dataclasses import dataclass
import hashlib, json
from datetime import datetime, timezone

@dataclass
class ChangeRecord:
    table: str
    op: str
    ts_ms: int
    pk: Dict[str, Any]
    before: Optional[Dict[str, Any]]
    after: Optional[Dict[str, Any]]
    event_id: str

def _hash(obj: Dict[str, Any]) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:32]

def parse_debezium_envelope(envelope: Dict[str, Any]) -> ChangeRecord:
    payload = envelope.get("payload") or envelope
    op = str(payload.get("op"))
    ts_ms = int(payload.get("ts_ms") or 0)
    src = payload.get("source") or {}
    schema = src.get("schema") or "public"
    table = src.get("table") or "unknown"
    full_table = f"{schema}.{table}"

    before = payload.get("before")
    after = payload.get("after")

    row = after or before or {}
    pk = {}
    if table == "customers" and "customer_id" in row:
        pk["customer_id"] = row["customer_id"]
    else:
        for k, v in row.items():
            if str(k).endswith("_id"):
                pk[k] = v
                break
    if not pk:
        raise ValueError("Unable to derive PK")

    event_id = _hash({"table": full_table, "ts_ms": ts_ms, "pk": pk, "op": op})
    return ChangeRecord(full_table, op, ts_ms, pk, before, after, event_id)

def ts_ms_to_dt(ts_ms: int) -> datetime:
    return datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc)
