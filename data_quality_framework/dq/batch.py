from typing import Any, Dict, List
import csv
from dq.rules import Ruleset
from dq.validators import validate_record, null_ratio, uniqueness_violations

def read_csv(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]

def run_batch_checks(rows: List[Dict[str, Any]], rules: Ruleset) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    total = len(rows)

    # row-level validation
    fail = 0
    sample = []
    for r in rows:
        ok, viol = validate_record(r, rules.fields)
        if not ok:
            fail += 1
            if len(sample) < 5:
                sample.append({"record": r, "violations": viol})
    results.append({"check_name":"row_validation","severity":"ERROR","passed":fail==0,"failed_count":fail,"total_count":total,"details":{"sample_failures":sample}})

    # uniqueness
    for keyset in (rules.batch.get("uniqueness", []) or []):
        dups = uniqueness_violations(rows, keyset)
        results.append({"check_name":f"uniqueness:{','.join(keyset)}","severity":"ERROR","passed":len(dups)==0,"failed_count":len(dups),"total_count":total,"details":{"sample_duplicates":dups[:5]}})

    # null ratios
    for field, max_ratio in (rules.batch.get("max_null_ratio", {}) or {}).items():
        ratio = null_ratio(rows, field)
        passed = ratio <= float(max_ratio)
        results.append({"check_name":f"null_ratio:{field}","severity":"WARN" if passed else "ERROR","passed":passed,"failed_count":int(ratio*total),"total_count":total,"details":{"null_ratio":ratio,"max_allowed":float(max_ratio)}})

    return results
