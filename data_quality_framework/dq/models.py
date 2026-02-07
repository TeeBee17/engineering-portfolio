import uuid
from sqlalchemy import Column, String, DateTime, Integer, JSON, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from dq.db import Base

class DQRun(Base):
    __tablename__ = "dq_runs"
    run_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset = Column(String(120), nullable=False)
    mode = Column(String(20), nullable=False)  # batch | stream
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    finished_at = Column(DateTime(timezone=True))
    status = Column(String(20), nullable=False, default="RUNNING")
    summary = Column(JSON, nullable=True)
    __table_args__ = (Index("idx_runs_dataset_started", "dataset", "started_at"),)

class DQCheckResult(Base):
    __tablename__ = "dq_check_results"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("dq_runs.run_id", ondelete="CASCADE"), nullable=False)
    dataset = Column(String(120), nullable=False)
    check_name = Column(String(120), nullable=False)
    severity = Column(String(20), nullable=False, default="WARN")  # INFO|WARN|ERROR
    passed = Column(Boolean, nullable=False)
    failed_count = Column(Integer, nullable=False, default=0)
    total_count = Column(Integer, nullable=False, default=0)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (Index("idx_results_run", "run_id"), Index("idx_results_dataset_created", "dataset", "created_at"))

class DQAlert(Base):
    __tablename__ = "dq_alerts"
    alert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey("dq_runs.run_id", ondelete="CASCADE"), nullable=False)
    dataset = Column(String(120), nullable=False)
    level = Column(String(20), nullable=False)  # WARN|ERROR
    message = Column(String(500), nullable=False)
    meta = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
