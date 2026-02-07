from __future__ import annotations
from typing import Any, Dict
import os
import duckdb

class DuckDBWarehouse:
    def __init__(self, db_path: str):
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self.con = duckdb.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        self.con.execute("""
        CREATE TABLE IF NOT EXISTS wh_customers (
          customer_id VARCHAR PRIMARY KEY,
          email VARCHAR,
          plan VARCHAR,
          country VARCHAR,
          status VARCHAR,
          updated_at TIMESTAMP,
          created_at TIMESTAMP
        );
        """)
        self.con.execute("""
        CREATE TABLE IF NOT EXISTS wh_applied_events (
          event_id VARCHAR PRIMARY KEY,
          applied_at TIMESTAMP DEFAULT NOW()
        );
        """)
        self.con.execute("""
        CREATE TABLE IF NOT EXISTS wh_checkpoints (
          topic VARCHAR,
          partition INTEGER,
          offset BIGINT,
          updated_at TIMESTAMP DEFAULT NOW(),
          PRIMARY KEY(topic, partition)
        );
        """)

    def already_applied(self, event_id: str) -> bool:
        return self.con.execute("SELECT 1 FROM wh_applied_events WHERE event_id=? LIMIT 1", [event_id]).fetchone() is not None

    def _checkpoint(self, meta: Dict[str, Any]) -> None:
        self.con.execute("""
        INSERT INTO wh_checkpoints(topic, partition, offset) VALUES (?, ?, ?)
        ON CONFLICT(topic, partition) DO UPDATE SET offset=EXCLUDED.offset, updated_at=NOW();
        """, [meta["topic"], int(meta["partition"]), int(meta["offset"])])

    def apply_customer_change(self, change: Dict[str, Any], meta: Dict[str, Any]) -> None:
        event_id = str(change["event_id"])
        if self.already_applied(event_id):
            self._checkpoint(meta)
            return

        op = change["op"]
        after = change.get("after") or {}
        before = change.get("before") or {}
        pk = change.get("pk") or {}
        customer_id = after.get("customer_id") or before.get("customer_id") or pk.get("customer_id")
        if not customer_id:
            raise ValueError("missing customer_id")

        if op in ("c", "u", "r"):
            self.con.execute("""
            INSERT INTO wh_customers(customer_id, email, plan, country, status, updated_at, created_at)
            VALUES (?, ?, ?, ?, ?, NOW(), NOW())
            ON CONFLICT(customer_id) DO UPDATE SET
              email=EXCLUDED.email,
              plan=EXCLUDED.plan,
              country=EXCLUDED.country,
              status=EXCLUDED.status,
              updated_at=NOW();
            """, [customer_id, after.get("email"), after.get("plan"), after.get("country"), after.get("status")])
        elif op == "d":
            self.con.execute("DELETE FROM wh_customers WHERE customer_id=?", [customer_id])

        self.con.execute("INSERT OR IGNORE INTO wh_applied_events(event_id) VALUES (?)", [event_id])
        self._checkpoint(meta)

    def query_customers(self, limit: int = 50):
        return self.con.execute("SELECT * FROM wh_customers ORDER BY updated_at DESC LIMIT ?", [limit]).fetchdf()

    def close(self):
        try:
            self.con.close()
        except Exception:
            pass
