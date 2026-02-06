from dataclasses import dataclass
from typing import Set, Iterable, Optional, Dict, Tuple
from app.auth import Principal

@dataclass
class AccessDecision:
    allowed_doc_ids: Set[int]
    reason: str

class PolicyEngine:
    """
    Simple RBAC + object rules.
    doc_acl_map[(tenant_id, doc_id)] = {
       "object_type": "case"|"kb"|"note",
       "object_id": "...",
       "visibility": "public"|"internal"|"restricted",
       "allowed_roles": {"admin","cs_agent"} ...
       "allowed_users": {"user1"} ...
    }
    """

    def __init__(self, doc_acl_map: Dict[Tuple[str, int], Dict]):
        self.doc_acl_map = doc_acl_map

    def authorize_docs(
        self,
        principal: Principal,
        candidate_doc_ids: Iterable[int],
        request_filters: Optional[Dict[str, str]] = None
    ) -> AccessDecision:
        allowed: Set[int] = set()
        tenant = principal.tenant_id

        filt_object_type = (request_filters or {}).get("object_type")

        for doc_id in candidate_doc_ids:
            meta = self.doc_acl_map.get((tenant, doc_id))
            if not meta:
                continue  # not in this tenant or unknown

            if filt_object_type and meta.get("object_type") != filt_object_type:
                continue

            visibility = meta.get("visibility", "internal")
            allowed_roles = set(meta.get("allowed_roles", []))
            allowed_users = set(meta.get("allowed_users", []))

            # Example policy
            if principal.role == "admin":
                allowed.add(doc_id)
                continue

            if visibility == "public":
                allowed.add(doc_id)
                continue

            if principal.user_id in allowed_users:
                allowed.add(doc_id)
                continue

            if principal.role in allowed_roles:
                allowed.add(doc_id)
                continue

        return AccessDecision(allowed_doc_ids=allowed, reason="RBAC/object policy applied")
