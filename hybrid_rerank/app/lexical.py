import re
from typing import List, Dict, Tuple, Optional
from rank_bm25 import BM25Okapi
from app.models import Doc

_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")

def tokenize(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]

class BM25Index:
    """BM25 over (title + body)."""
    def __init__(self):
        self.doc_ids: List[int] = []
        self.corpus_tokens: List[List[str]] = []
        self._bm25: Optional[BM25Okapi] = None

    def build(self, docs: List[Doc]) -> None:
        self.doc_ids = [d.doc_id for d in docs]
        self.corpus_tokens = [tokenize(d.title + " " + d.body) for d in docs]
        self._bm25 = BM25Okapi(self.corpus_tokens)

    def search(self, query: str, k: int, filter_object_type: Optional[str] = None, docs_by_id: Dict[int, Doc] = None) -> List[Tuple[int, float]]:
        if not self._bm25:
            return []
        q = tokenize(query)
        scores = self._bm25.get_scores(q)

        pairs = list(zip(self.doc_ids, scores))
        pairs.sort(key=lambda x: x[1], reverse=True)

        if filter_object_type and docs_by_id:
            out = []
            for doc_id, s in pairs:
                d = docs_by_id.get(doc_id)
                if d and d.object_type == filter_object_type:
                    out.append((doc_id, float(s)))
                if len(out) >= k:
                    break
            return out

        return [(doc_id, float(s)) for doc_id, s in pairs[:k]]
