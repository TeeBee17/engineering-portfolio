# Batch + Streaming Data Quality Framework

A portfolio-ready reference implementation of a **data quality system** that supports both:

- **Batch validation** (files, warehouse extracts, daily snapshots)
- **Streaming validation** (Kafka topics, near real-time event pipelines)

It demonstrates how modern enterprises enforce **data correctness, freshness, and reliability** across the full lifecycle of data — from ingestion to downstream analytics and AI.

---

## Problem Statement

In real production systems, data pipelines break in ways that are **subtle, expensive, and hard to detect**.

### Common real-world failures
- Required fields suddenly become null (e.g., `customer_id`)
- Upstream services start emitting invalid enums (e.g., `status="UNKNOWN"`)
- Amounts go negative due to bugs or currency conversion issues
- Duplicate primary keys appear due to retries or idempotency bugs
- Events arrive late (streaming lag), making downstream systems stale
- Bad data silently contaminates:
  - dashboards
  - ML features
  - customer-facing agents (RAG/LLM grounding)
  - revenue and billing pipelines

### Why batch-only checks are not enough
Batch checks catch problems *after the fact* (hours later).
For customer-facing AI systems, you need **streaming checks** to detect issues in minutes.

---

## How this repo solves the problem

This repo implements a lightweight but complete framework that:

### ✅ Enforces schema + constraints
- Required fields
- Type checks
- Range checks (`min/max`)
- Enum checks
- Regex checks (optional)

### ✅ Supports both batch + streaming
- Batch checks run against a file input (CSV demo)
- Streaming checks run continuously against Kafka events

### ✅ Captures results + alerts
- Every run is stored in Postgres
- Every check result is stored with metadata
- Alerts are derived automatically when checks fail

### ✅ Provides an API for observability
FastAPI exposes:
- `/runs`
- `/runs/{id}/results`
- `/runs/{id}/alerts`

---

## Repository Structure (What each file does)

### `config/`
- **`config/rules.yaml`**
  - Central rule definition file
  - Used by both batch and streaming validators

### `dq/` (core framework)
- **`dq/rules.py`**
  - Loads YAML rules into a strongly-typed ruleset

- **`dq/validators.py`**
  - Core rule engine:
    - required checks
    - type checks
    - enum checks
    - range checks
    - regex checks
  - Also includes:
    - null ratio computation
    - uniqueness detection (batch)

- **`dq/batch.py`**
  - Batch pipeline:
    - loads CSV
    - validates each row
    - runs uniqueness + null ratio checks
    - returns structured check results

- **`dq/stream.py`**
  - Kafka consumer validator:
    - reads JSON events from Kafka
    - validates each event
    - checks event-time lag/freshness (`max_lag_seconds`)
    - returns structured check results

- **`dq/alerts.py`**
  - Converts failed checks into alerts
  - Produces human-readable messages (like a real ops system)

- **`dq/models.py`**
  - Postgres schema using SQLAlchemy ORM:
    - runs
    - check results
    - alerts

- **`dq/repo.py`**
  - Persistence layer:
    - create run
    - write results
    - write alerts
    - finish run with summary

- **`dq/api.py`**
  - FastAPI app exposing observability endpoints

- **`dq/producer.py`**
  - Kafka producer that generates sample `orders` events
  - Intentionally emits bad events sometimes (to demonstrate failures)

- **`dq/cli.py`**
  - Unified CLI entrypoint:
    - `batch`
    - `stream`
    - `produce`

### `tests/`
- Unit tests proving correctness:
  - validator correctness
  - batch uniqueness + null ratio logic

---

## Tech Stack
- Python 3.11
- Kafka (Confluent image via Docker Compose)
- Postgres 15
- FastAPI + SQLAlchemy
- PyYAML for rules
- pytest

---

## Quickstart

### 1) Start Kafka + Postgres
```bash
docker compose up -d
```

### 2) Create the Kafka topic
```bash
docker exec -it $(docker ps -qf name=dq_kafka) bash -lc \
  "kafka-topics --create --topic orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 || true"
```

### 3) Produce sample events
```bash
python -m dq.cli produce --topic orders --count 50
```

### 4) Run streaming validation (Kafka consumer)
```bash
python -m dq.cli stream --topic orders --group dq-consumer --max-messages 50
```

### 5) Run batch validation (CSV)
```bash
python -m dq.cli batch --input data/sample_orders.csv
```

### 6) Start the API
```bash
uvicorn dq.api:app --reload --port 8000
```

Then open:
- http://127.0.0.1:8000/docs

---

## Example Rules
Rules live in:
- `config/rules.yaml`

Example enforced rules:
- `amount` must be between 0 and 1,000,000
- `currency` must be one of `NGN/USD/EUR`
- `status` must be one of allowed enums
- `created_at` must be ISO datetime
- streaming lag must be <= 10 minutes

---

## Technical Value
This project demonstrates:
- Designing a quality framework usable for both batch + streaming
- Rule-driven validation with reusable checks
- Production-style persistence and observability
- Kafka consumer architecture for real-time enforcement
- Operational thinking: freshness, lag, alerts, auditability

---

## Next Extensions (Optional)
- Integrate Great Expectations or AWS Deequ
- Add Slack/Email alert integrations
- Add Prometheus metrics exporter
- Add schema registry (Avro/Protobuf)
- Add distributed execution (Spark / Flink)
