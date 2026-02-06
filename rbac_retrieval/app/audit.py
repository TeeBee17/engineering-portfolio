import json
from datetime import datetime, timezone
from typing import Dict, Any
from app.config import settings

def audit_log(tenant_id: str, user_id: str, role: str, action: str, detail: Dict[str, Any]) -> None:
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "tenant_id": tenant_id,
        "user_id": user_id,
        "role": role,
        "action": action,
        "detail": detail
    }
    with open(settings.AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
