from fastapi.testclient import TestClient
from app.api import app
from app.seed import main as seed_main

def test_hybrid_returns_results():
    seed_main()
    client = TestClient(app)

    r = client.post("/search", json={"query": "reset password", "top_k": 5, "use_rerank": False})
    assert r.status_code == 200
    data = r.json()
    assert len(data["hits"]) > 0
