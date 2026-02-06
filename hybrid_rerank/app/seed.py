from app.models import Doc
from app.api import store, rebuild_indexes

def main():
    docs = [
        Doc(doc_id=1, title="Reset password steps", body="If user forgot password, send reset link and verify email.", object_type="kb", object_id="KB-100"),
        Doc(doc_id=2, title="Reset MFA for admin users", body="Admin MFA reset requires identity verification and device re-enrollment.", object_type="kb", object_id="KB-220"),
        Doc(doc_id=3, title="Login loop after SSO", body="Clear cookies; check IdP session; verify redirect URI configuration.", object_type="kb", object_id="KB-310"),
        Doc(doc_id=4, title="CASE-900: cannot login; MFA token expired", body="Customer locked out due to expired MFA token; reset and re-enroll device.", object_type="case", object_id="CASE-900"),
        Doc(doc_id=5, title="CASE-901: billing refund request", body="Customer requested refund; validate invoice and process credit memo.", object_type="case", object_id="CASE-901"),
        Doc(doc_id=6, title="VIP escalation playbook", body="Escalate VIP accounts to Tier-3; notify incident commander; follow comms template.", object_type="note", object_id="NOTE-77"),
        Doc(doc_id=7, title="Admin password reset", body="Admins can reset passwords in settings; ensure policy compliance.", object_type="kb", object_id="KB-130"),
        Doc(doc_id=8, title="Device re-enrollment procedure", body="Re-enroll device for MFA: revoke old factors, generate enrollment QR, verify with user.", object_type="kb", object_id="KB-401"),
    ]
    for d in docs:
        store.upsert(d)

    rebuild_indexes()
    print("Seeded docs and built BM25 + FAISS indexes.")
    print("Run: uvicorn app.api:app --reload")

if __name__ == "__main__":
    main()
