# Database-to-Data-Warehouse CDC Pipeline (Postgres + Debezium → Kafka → Lake/Warehouse)

A portfolio-ready **Change Data Capture (CDC)** reference implementation that streams row-level changes from an **OLTP database**
into an analytics **lake/warehouse** with:

- near-real-time ingestion
- replay-safe **idempotent merges**
- INSERT/UPDATE/DELETE propagation
- bronze (append-only) + silver (merged) layers

This project uses **Debezium** to capture Postgres WAL changes and publish them to Kafka.
A Python consumer then lands:
1) raw change events into a Parquet “bronze” lake for audit/replay
2) merged tables into DuckDB (“silver”) for fast analytics queries

---

## Problem Statement

Batch ETL often leads to stale data, expensive full scans, and hard-to-handle updates/deletes.
CDC solves this by streaming incremental changes (WAL/binlog) into Kafka, then materializing
warehouse tables with **idempotent upserts**.

---

## Architecture

Postgres (logical replication/WAL)
  → Debezium Postgres Connector
  → Kafka topic: `dbserver1.public.customers` (Debezium envelope)
  → Python CDC consumer
      - Bronze: Parquet append-only events
      - Silver: DuckDB merged table (`wh_customers`)

---

## Repo Structure (What each file does)

### Infra (`infra/`)
- `infra/docker-compose.yml` — Postgres (logical WAL), Kafka, Debezium Connect
- `infra/initdb/01_create_tables.sql` — demo source table + seed rows
- `infra/connectors/debezium-postgres-customers.json` — Debezium connector config

### Consumer (`cdc_pipeline/`)
- `config.py` — Kafka/topic + output paths
- `debezium.py` — parses Debezium envelope into normalized ChangeRecord + stable `event_id`
- `lake.py` — appends raw change records to partitioned Parquet
- `warehouse_duckdb.py` — **idempotent merge** into DuckDB + applied-event ledger + checkpoints
- `consumer.py` — Kafka consume loop; commits offsets after durable writes
- `http.py` — tiny helper for Connect REST calls
- `cli.py` — commands: register connector, seed DB, consume, query

### Tests
- `tests/test_debezium_parser.py` — validates create/update/delete parsing
- `tests/test_duckdb_merge.py` — validates idempotency + delete handling

---

## Quickstart

### 1) Start infra
```bash
docker compose -f infra/docker-compose.yml up -d
```

### 2) Register the Debezium connector
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m cdc_pipeline.cli register-connector \
  --connect-url http://localhost:8083 \
  --config infra/connectors/debezium-postgres-customers.json
```

### 3) Create some changes
```bash
python -m cdc_pipeline.cli seed --pg-url postgresql+psycopg2://cdc:cdc@localhost:5432/cdc
```

### 4) Run the consumer
```bash
python -m cdc_pipeline.cli consume --topic dbserver1.public.customers
```

### 5) Query the warehouse
```bash
python -m cdc_pipeline.cli query --limit 20
```

---

## Outputs

- Bronze lake: `warehouse/lake/customers/date=YYYY-MM-DD/*.parquet`
- Silver warehouse: `warehouse/warehouse.duckdb` (table: `wh_customers`)

---

## Resume-ready highlights

- Implemented Debezium-based CDC from Postgres WAL to Kafka
- Built replay-safe consumer with idempotent merges and delete propagation
- Landed raw CDC events to Parquet for audit/replay and materialized analytics tables in DuckDB
- Automated connector registration via Kafka Connect REST API
