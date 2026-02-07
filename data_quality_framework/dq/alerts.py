from typing import Dict, List

def derive_alerts(dataset: str, results: List[Dict]) -> List[Dict]:
    alerts: List[Dict] = []
    for r in results:
        if not r["passed"]:
            level = "ERROR" if r["severity"] == "ERROR" else "WARN"
            alerts.append({
                "level": level,
                "message": f"{dataset} check failed: {r['check_name']} ({r['failed_count']}/{r['total_count']})",
                "meta": r.get("details", {})
            })
    return alerts
