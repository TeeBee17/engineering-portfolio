# RBAC-safe Multi-tenant Retrieval (FAISS + FastAPI)

This is a reference implementation of a "permission-first" retrieval layer:
- Multi-tenant isolation by tenant_id
- RBAC/object rules applied BEFORE vector scoring
- Audit logging
- Tests to prevent cross-tenant leakage

## Use Case
RBAC-Safe Multi-Tenant Retrieval (No Data Leakage)
Real-life use case

When an AI agent searches across cases, tickets, internal docs, Slack/Teams, CRM notes, etc., it must never return something the user doesn’t have access to.

Why it matters

Prevents cross-customer data leaks (catastrophic in enterprise SaaS)

Required for SOC2, ISO, GDPR, and customer trust

Especially critical in multi-tenant platforms like Salesforce

## Run locally
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Seed data and start
python -m app.seed
uvicorn app.main:app --reload

## Try queries
curl -s -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tenantA:user1:role=cs_agent" \
  -d '{"query":"reset password", "top_k":5}'

## Run tests
pytest -q

## Notes
This demo uses an in-memory FAISS index and a toy embedding function for determinism.
In production you would use a real embedding model and persist indices (or use a vector DB).
