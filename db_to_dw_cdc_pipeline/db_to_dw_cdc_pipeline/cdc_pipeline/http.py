from __future__ import annotations
from typing import Any, Dict
import requests

def post_json(url: str, payload: Dict[str, Any], timeout: int = 20) -> Dict[str, Any]:
    r = requests.post(url, json=payload, timeout=timeout)
    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text}")
    try:
        return r.json()
    except Exception:
        return {"status": r.status_code, "text": r.text}
