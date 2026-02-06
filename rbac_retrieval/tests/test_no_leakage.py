import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.seed import main as seed_main

@pytest.fixture(scope="session", autouse=True)
def seed():
    seed_main()

def test_tenant_isolation_no_cross_tenant_docs():
    client = TestClient(app)

    r = client.post(
        "/search",
        headers={"Authorization": "Bearer tenantA:user1:role=cs_agent"},
        json={"query": "TenantB password reset", "top_k": 5}
    )
    assert r.status_code == 200
    data = r.json()
    assert data["tenant_id"] == "tenantA"

    returned_ids = [h["doc_id"] for h in data["hits"]]
    assert all(doc_id < 10 for doc_id in returned_ids), f"Leakage detected: {returned_ids}"
