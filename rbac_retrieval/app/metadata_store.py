import sqlite3
from typing import List, Dict, Tuple, Optional
from app.config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS docs (
  tenant_id TEXT NOT NULL,
  doc_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  visibility TEXT NOT NULL,
  allowed_roles TEXT NOT NULL,  -- comma-separated
  allowed_users TEXT NOT NULL,  -- comma-separated
  PRIMARY KEY (tenant_id, doc_id)
);
"""

class MetadataStore:
    def __init__(self, db_path: str = settings.DB_PATH):
        self.db_path = db_path
        self._init()

    def _init(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(SCHEMA)
            conn.commit()

    def upsert_doc(self, tenant_id: str, doc_id: int, title: str,
                   object_type: str, object_id: str, visibility: str,
                   allowed_roles: List[str], allowed_users: List[str]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO docs (tenant_id, doc_id, title, object_type, object_id, visibility, allowed_roles, allowed_users)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(tenant_id, doc_id) DO UPDATE SET
                  title=excluded.title,
                  object_type=excluded.object_type,
                  object_id=excluded.object_id,
                  visibility=excluded.visibility,
                  allowed_roles=excluded.allowed_roles,
                  allowed_users=excluded.allowed_users
                """,
                (
                    tenant_id, doc_id, title, object_type, object_id, visibility,
                    ",".join(allowed_roles), ",".join(allowed_users)
                )
            )
            conn.commit()

    def get_doc(self, tenant_id: str, doc_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT tenant_id, doc_id, title, object_type, object_id, visibility, allowed_roles, allowed_users FROM docs WHERE tenant_id=? AND doc_id=?",
                (tenant_id, doc_id)
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "tenant_id": row[0],
                "doc_id": row[1],
                "title": row[2],
                "object_type": row[3],
                "object_id": row[4],
                "visibility": row[5],
                "allowed_roles": set([r for r in row[6].split(",") if r]),
                "allowed_users": set([u for u in row[7].split(",") if u]),
            }

    def load_acl_map(self) -> Dict[Tuple[str, int], Dict]:
        acl_map: Dict[Tuple[str, int], Dict] = {}
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT tenant_id, doc_id, object_type, object_id, visibility, allowed_roles, allowed_users FROM docs"
            )
            for tenant_id, doc_id, object_type, object_id, visibility, roles, users in cur.fetchall():
                acl_map[(tenant_id, doc_id)] = {
                    "object_type": object_type,
                    "object_id": object_id,
                    "visibility": visibility,
                    "allowed_roles": set([r for r in roles.split(",") if r]),
                    "allowed_users": set([u for u in users.split(",") if u]),
                }
        return acl_map

    def bulk_list_doc_ids(self, tenant_id: str) -> List[int]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT doc_id FROM docs WHERE tenant_id=?", (tenant_id,))
            return [r[0] for r in cur.fetchall()]
