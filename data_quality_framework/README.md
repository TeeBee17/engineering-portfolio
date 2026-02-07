# Batch + Streaming Data Quality Framework

Portfolio-ready reference implementation supporting:
- **Batch checks** on files (CSV demo)
- **Streaming checks** on Kafka topics (schema + constraints + freshness lag)
- **YAML rule engine**
- **Results + alerts** persisted to Postgres
- **FastAPI** for querying runs/results/alerts

## Quickstart
```bash
docker compose up -d

docker exec -it $(docker ps -qf name=dq_kafka) bash -lc "kafka-topics --create --topic orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 || true"
python -m dq.cli produce --topic orders --count 50
python -m dq.cli stream --topic orders --group dq-consumer --max-messages 50
python -m dq.cli batch --input data/sample_orders.csv

uvicorn dq.api:app --reload --port 8000
# open http://127.0.0.1:8000/docs
```

Rules: `config/rules.yaml`
