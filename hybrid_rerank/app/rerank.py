import re
from typing import Dict, List, Tuple
from app.models import Doc
from app.config import settings

_WORD = re.compile(r"[A-Za-z0-9]+")

def _tokens(text: str) -> List[str]:
    return [t.lower() for t in _WORD.findall(text)]

def _phrase_hit(query: str, text: str) -> float:
    q = query.strip().lower()
    t = text.lower()
    if q and q in t:
        return 1.0
    qt = _tokens(q)
    if len(qt) < 2:
        return 0.0
    bigrams = set(zip(qt, qt[1:]))
    tt = _tokens(t)
    tbigrams = set(zip(tt, tt[1:]))
    if not bigrams:
        return 0.0
    return len(bigrams & tbigrams) / len(bigrams)

def _overlap(query: str, text: str) -> float:
    q = set(_tokens(query))
    if not q:
        return 0.0
    t = set(_tokens(text))
    return len(q & t) / len(q)

def rerank(query: str, candidates: Dict[int, Dict[str, float]], docs_by_id: Dict[int, Doc]) -> List[Tuple[int, float]]:
    """Lightweight reranker: final = a*hybrid + b*phrase + c*overlap."""
    out: List[Tuple[int, float]] = []
    for doc_id, scores in candidates.items():
        d = docs_by_id.get(doc_id)
        if not d:
            continue

        text = f"{d.title}\n{d.body}"
        phrase = _phrase_hit(query, text)
        overlap = _overlap(query, text)
        hybrid = float(scores["hybrid_score"])

        final = (
            settings.RERANK_W_HYBRID * hybrid
            + settings.RERANK_W_PHRASE * phrase
            + settings.RERANK_W_OVERLAP * overlap
        )
        out.append((doc_id, float(final)))

    out.sort(key=lambda x: x[1], reverse=True)
    return out
