from typing import Dict, List, Optional
from app.models import Doc

class InMemoryDocStore:
    def __init__(self):
        self.docs_by_id: Dict[int, Doc] = {}

    def upsert(self, doc: Doc) -> None:
        self.docs_by_id[doc.doc_id] = doc

    def get(self, doc_id: int) -> Optional[Doc]:
        return self.docs_by_id.get(doc_id)

    def all_docs(self) -> List[Doc]:
        return list(self.docs_by_id.values())
