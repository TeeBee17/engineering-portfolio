import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.seed import main as seed_main

@pytest.fixture(scope="session", autouse=True)
def seed():
    seed_main()

def test_restricted_doc_requires_admin_or_allowed_user():
    client = TestClient(app)

    r1 = client.post(
        "/search",
        headers={"Authorization": "Bearer tenantA:user1:role=cs_agent"},
        json={"query": "VIP escalation", "top_k": 10}
    )
    assert r1.status_code == 200
    ids1 = [h["doc_id"] for h in r1.json()["hits"]]
    assert 2 in ids1

    r2 = client.post(
        "/search",
        headers={"Authorization": "Bearer tenantA:user2:role=cs_agent"},
        json={"query": "VIP escalation", "top_k": 10}
    )
    assert r2.status_code == 200
    ids2 = [h["doc_id"] for h in r2.json()["hits"]]
    assert 2 not in ids2

    r3 = client.post(
        "/search",
        headers={"Authorization": "Bearer tenantA:admin1:role=admin"},
        json={"query": "VIP escalation", "top_k": 10}
    )
    assert r3.status_code == 200
    ids3 = [h["doc_id"] for h in r3.json()["hits"]]
    assert 2 in ids3
