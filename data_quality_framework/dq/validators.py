from typing import Any, Dict, List, Tuple
import re
from dateutil import parser as dtparser

def _is_number(x: Any) -> bool:
    try:
        float(x)
        return True
    except Exception:
        return False

def validate_record(record: Dict[str, Any], field_rules: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
    violations: List[Dict[str, Any]] = []
    for field, rules in field_rules.items():
        val = record.get(field)

        if rules.get("required") and (val is None or val == ""):
            violations.append({"field": field, "rule": "required", "message": "missing required field"})
            continue

        if val is None or val == "":
            continue

        typ = rules.get("type")
        if typ == "string":
            if not isinstance(val, str):
                violations.append({"field": field, "rule": "type", "expected": "string"})
        elif typ == "number":
            if not _is_number(val):
                violations.append({"field": field, "rule": "type", "expected": "number"})
            else:
                f = float(val)
                if "min" in rules and f < float(rules["min"]):
                    violations.append({"field": field, "rule": "min", "min": rules["min"], "value": f})
                if "max" in rules and f > float(rules["max"]):
                    violations.append({"field": field, "rule": "max", "max": rules["max"], "value": f})
        elif typ == "datetime_iso":
            try:
                dtparser.isoparse(str(val))
            except Exception:
                violations.append({"field": field, "rule": "type", "expected": "datetime_iso"})
        elif typ:
            violations.append({"field": field, "rule": "type", "expected": typ, "message": "unknown type in rules"})

        if "enum" in rules and val not in rules["enum"]:
            violations.append({"field": field, "rule": "enum", "allowed": rules["enum"], "value": val})

        if "regex" in rules:
            if not re.fullmatch(rules["regex"], str(val)):
                violations.append({"field": field, "rule": "regex", "pattern": rules["regex"], "value": val})

    return (len(violations) == 0, violations)

def null_ratio(rows: List[Dict[str, Any]], field: str) -> float:
    if not rows:
        return 0.0
    nulls = sum(1 for r in rows if r.get(field) in (None, ""))
    return nulls / len(rows)

def uniqueness_violations(rows: List[Dict[str, Any]], keys: List[str]) -> List[Dict[str, Any]]:
    seen = set()
    dups = []
    for r in rows:
        k = tuple(r.get(x) for x in keys)
        if k in seen:
            dups.append({"keys": keys, "value": k, "record": r})
        else:
            seen.add(k)
    return dups
