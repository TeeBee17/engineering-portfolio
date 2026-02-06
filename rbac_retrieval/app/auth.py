from dataclasses import dataclass

@dataclass(frozen=True)
class Principal:
    tenant_id: str
    user_id: str
    role: str

def parse_bearer_token(auth_header: str) -> Principal:
    """
    Demo token format:
      Bearer tenantA:user1:role=cs_agent

    In real life, validate a JWT and extract claims.
    """
    if not auth_header or not auth_header.startswith("Bearer "):
        raise ValueError("Missing/invalid Authorization header")

    token = auth_header[len("Bearer "):].strip()
    try:
        tenant_part, user_part, role_part = token.split(":")
        if not role_part.startswith("role="):
            raise ValueError
        role = role_part.split("=", 1)[1]
        return Principal(tenant_id=tenant_part, user_id=user_part, role=role)
    except Exception:
        raise ValueError("Invalid token format")
