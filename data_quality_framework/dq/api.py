from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dq.db import SessionLocal, init_db
from dq import repo

app = FastAPI(title="Data Quality Framework API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/runs")
def list_runs(dataset: str | None = None, limit: int = 50, db: Session = Depends(get_db)):
    runs = repo.list_runs(db, dataset=dataset, limit=limit)
    return [{
        "run_id": str(r.run_id),
        "dataset": r.dataset,
        "mode": r.mode,
        "status": r.status,
        "started_at": r.started_at,
        "finished_at": r.finished_at,
        "summary": r.summary,
    } for r in runs]

@app.get("/runs/{run_id}/results")
def get_results(run_id: str, db: Session = Depends(get_db)):
    res = repo.run_results(db, run_id)
    return [{
        "check_name": r.check_name,
        "severity": r.severity,
        "passed": r.passed,
        "failed_count": r.failed_count,
        "total_count": r.total_count,
        "details": r.details,
        "created_at": r.created_at,
    } for r in res]

@app.get("/runs/{run_id}/alerts")
def get_alerts(run_id: str, db: Session = Depends(get_db)):
    als = repo.run_alerts(db, run_id)
    return [{
        "level": a.level,
        "message": a.message,
        "meta": a.meta,
        "created_at": a.created_at,
    } for a in als]
