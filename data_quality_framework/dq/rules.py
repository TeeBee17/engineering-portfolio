from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import yaml
from dq.config import settings

@dataclass
class Ruleset:
    dataset: str
    description: str
    primary_key: List[str]
    fields: Dict[str, Dict[str, Any]]
    streaming: Dict[str, Any]
    batch: Dict[str, Any]

def load_rules(path: Optional[str] = None) -> Ruleset:
    p = path or settings.RULES_PATH
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Ruleset(
        dataset=data["dataset"],
        description=data.get("description", ""),
        primary_key=data.get("primary_key", []),
        fields=data.get("fields", {}),
        streaming=data.get("streaming", {}),
        batch=data.get("batch", {}),
    )
