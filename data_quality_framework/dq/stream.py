from typing import Any, Dict, List, Optional
import json, time
from dateutil import parser as dtparser
from confluent_kafka import Consumer
from dq.rules import Ruleset
from dq.validators import validate_record

def _event_lag_seconds(event_time_iso: str, now_ts: float) -> Optional[float]:
    try:
        et = dtparser.isoparse(event_time_iso)
        return max(0.0, now_ts - et.timestamp())
    except Exception:
        return None

def stream_consume_and_validate(rules: Ruleset, topic: str, bootstrap: str, group: str, max_messages: int = 0) -> List[Dict[str, Any]]:
    c = Consumer({"bootstrap.servers": bootstrap, "group.id": group, "auto.offset.reset": "earliest", "enable.auto.commit": True})
    c.subscribe([topic])

    event_time_field = rules.streaming.get("event_time_field", "")
    max_lag = float(rules.streaming.get("max_lag_seconds", 0) or 0)

    total = bad = lag_bad = 0
    samples = []
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue

            total += 1
            try:
                rec = json.loads(msg.value().decode("utf-8"))
            except Exception:
                bad += 1
                if len(samples) < 5:
                    samples.append({"raw": (msg.value() or b"")[:200].decode("utf-8","ignore"), "violations":[{"rule":"json","message":"invalid json"}]})
                if max_messages and total >= max_messages:
                    break
                continue

            ok, viol = validate_record(rec, rules.fields)
            if not ok:
                bad += 1
                if len(samples) < 5:
                    samples.append({"record": rec, "violations": viol})

            if event_time_field and max_lag > 0:
                lag = _event_lag_seconds(str(rec.get(event_time_field,"")), time.time())
                if lag is None or lag > max_lag:
                    lag_bad += 1
                    if len(samples) < 5:
                        samples.append({"record": rec, "violations":[{"rule":"lag","max_lag_seconds":max_lag,"lag_seconds":lag}]})

            if max_messages and total >= max_messages:
                break
    finally:
        c.close()

    out = [{
        "check_name":"stream_row_validation",
        "severity":"ERROR",
        "passed": bad == 0,
        "failed_count": bad,
        "total_count": total,
        "details":{"sample_failures": samples[:5]},
    }]
    if event_time_field and max_lag > 0:
        out.append({
            "check_name":f"freshness_lag:{event_time_field}",
            "severity":"WARN" if lag_bad == 0 else "ERROR",
            "passed": lag_bad == 0,
            "failed_count": lag_bad,
            "total_count": total,
            "details":{"max_lag_seconds": max_lag},
        })
    return out
