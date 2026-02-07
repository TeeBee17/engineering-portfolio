from __future__ import annotations
from typing import Dict, Any
import json
from confluent_kafka import Consumer
from cdc_pipeline.config import settings
from cdc_pipeline.debezium import parse_debezium_envelope
from cdc_pipeline.lake import ParquetLake
from cdc_pipeline.warehouse_duckdb import DuckDBWarehouse

def consume(topic: str | None = None, group: str | None = None, max_messages: int = 0) -> Dict[str, Any]:
    topic = topic or settings.topic
    group = group or settings.group

    c = Consumer({
        "bootstrap.servers": settings.kafka_bootstrap,
        "group.id": group,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    })
    c.subscribe([topic])

    lake = ParquetLake(settings.lake_customers_dir)
    wh = DuckDBWarehouse(settings.duckdb_path)

    processed = 0
    bad = 0

    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue

            processed += 1
            try:
                env = json.loads(msg.value().decode("utf-8"))
                ch = parse_debezium_envelope(env)
                rec = {
                    "event_id": ch.event_id,
                    "table": ch.table,
                    "op": ch.op,
                    "ts_ms": ch.ts_ms,
                    "pk": ch.pk,
                    "before": ch.before,
                    "after": ch.after,
                }
                lake.append_change(rec)
                wh.apply_customer_change(rec, {"topic": msg.topic(), "partition": msg.partition(), "offset": msg.offset()})
                c.commit(message=msg, asynchronous=False)
            except Exception:
                bad += 1
                c.commit(message=msg, asynchronous=False)

            if max_messages and processed >= max_messages:
                break
    finally:
        c.close()
        wh.close()

    return {"processed": processed, "bad": bad, "topic": topic, "duckdb": settings.duckdb_path, "lake": settings.lake_customers_dir}
