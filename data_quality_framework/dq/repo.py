from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from dq.models import DQRun, DQCheckResult, DQAlert

def create_run(db: Session, dataset: str, mode: str) -> DQRun:
    run = DQRun(dataset=dataset, mode=mode, status="RUNNING")
    db.add(run); db.commit(); db.refresh(run)
    return run

def finish_run(db: Session, run_id, status: str, summary: Dict) -> None:
    run = db.get(DQRun, run_id)
    run.status = status
    run.summary = summary
    from sqlalchemy.sql import func
    run.finished_at = func.now()
    db.commit()

def add_results(db: Session, run_id, dataset: str, results: List[Dict]) -> None:
    for r in results:
        db.add(DQCheckResult(
            run_id=run_id, dataset=dataset,
            check_name=r["check_name"], severity=r["severity"],
            passed=bool(r["passed"]),
            failed_count=int(r["failed_count"]),
            total_count=int(r["total_count"]),
            details=r.get("details"),
        ))
    db.commit()

def add_alerts(db: Session, run_id, dataset: str, alerts: List[Dict]) -> None:
    for a in alerts:
        db.add(DQAlert(run_id=run_id, dataset=dataset, level=a["level"], message=a["message"], meta=a.get("meta")))
    db.commit()

def list_runs(db: Session, dataset: Optional[str] = None, limit: int = 50):
    q = db.query(DQRun)
    if dataset:
        q = q.filter(DQRun.dataset == dataset)
    return q.order_by(DQRun.started_at.desc()).limit(limit).all()

def run_results(db: Session, run_id):
    return db.query(DQCheckResult).filter(DQCheckResult.run_id == run_id).order_by(DQCheckResult.created_at.asc()).all()

def run_alerts(db: Session, run_id):
    return db.query(DQAlert).filter(DQAlert.run_id == run_id).order_by(DQAlert.created_at.asc()).all()
