from fastapi.testclient import TestClient
from app.api import app
from app.seed import main as seed_main

def test_reranker_boosts_phrase_match_for_mfa_admin():
    seed_main()
    client = TestClient(app)

    r1 = client.post("/search", json={"query": "reset MFA for admin", "top_k": 3, "use_rerank": False})
    assert r1.status_code == 200
    hits1 = r1.json()["hits"]
    assert len(hits1) > 0

    r2 = client.post("/search", json={"query": "reset MFA for admin", "top_k": 3, "use_rerank": True})
    assert r2.status_code == 200
    hits2 = r2.json()["hits"]
    assert len(hits2) > 0
    top2 = hits2[0]["object_id"]

    assert top2 == "KB-220"
