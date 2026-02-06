# Engineering Portfolio (15+ Years)

This repository is a curated collection of engineering, streaming, analytics, and distributed systems projects I’ve built over the last 15+ years.

The focus of this portfolio is on:
- scalable data pipelines (batch + streaming)
- distributed systems and platform thinking
- data modeling and analytics enablement
- experimentation and metric reliability
- production-grade engineering practices (testing, observability, documentation)

---

## Projects

### 1) Member Messaging Feature Store
**Tech:** Apache Flink, Kafka (MSK-compatible), Java, Docker  
A real-time feature store that merges recent user activity and messaging history to generate unified per-member messaging features for eligibility, suppression, dashboards, and experimentation.

<a href="https://github.com/TeeBee17/engineering-portfolio/tree/main/Member%20Messaging%20Feature%20Store">
📁 member-messaging-feature-store
</a>
<br>


### 2) Experimentation Metrics Framework
**Tech:** Spark, SQL, Python  
Reusable metrics pipeline for A/B testing with standardized exposure/outcome modeling and metric definitions.

<a href="https://github.com/TeeBee17/engineering-portfolio/tree/main/Experimentation%20Metrics%20Framework">
📁 experimentation-metrics-framework
</a>
<br>

### 3) Batch + Streaming Data Quality Framework
**Tech:** Great Expectations / custom checks, Spark, SQL  
Automated data audits, anomaly detection, and freshness checks for large-scale datasets.

📁 `data-quality-framework/`

---

### 4) CDC Pipeline for Warehouse Ingestion
**Tech:** Debezium, Kafka, Postgres, S3, Glue  
Change Data Capture pipeline for syncing operational databases into an analytics warehouse.

📁 `cdc-pipeline-debezium/`

---

### 5) Spark Performance + Cost Optimization Toolkit
**Tech:** Spark, Scala, AWS  
Tools and examples for tuning Spark workloads, reducing shuffle, and improving cluster efficiency.

📁 `spark-optimization-toolkit/`

---

### 6) High-Throughput Event Aggregator 
**Tech:** Kafka & Kotlin
Service that consumes a high-volume stream of "transaction" events from Kafka and aggregates them into time-series windows (e.g., total spend per category every minute).

Focus: Implement "exactly-once" processing semantics and handle late-arriving data.

Use Case: Kafka and the real-time data processing that can be used for Risk and Applied AI.

📁 `High-Throughput-Event-Aggregator/`
---

### 7) Database-to-Data-Warehouse CDC Pipeline (Python & Spark): a Change Data Capture (CDC) pipeline that monitors a relational database (PostgreSQL) and incrementally syncs changes to a simulated Data Lake (Parquet files) or Snowflake.

Focus: Schema evolution and data integrity checks.

Use Case : Data Integrations and Transformations

📁 `Database-to-Data-Warehouse/`

---

### 8) GraphQL Wrapper for Legacy APIs (Java/Spring Boot): GraphQL gateway that aggregates data from three different "messy" REST APIs (e.g., Weather, Finnhub, and Twitter) into a clean, unified schema.

Focus: Implement dataloaders to solve the $N+1$ query problem and add a caching layer with Redis.

Use Case: "abstract the nuances of raw data access" for other developers.

📁 `GraphQL Wrapper for Legacy APIs/`
---

### 9) Distributed Rate Limiter (Java & Redis): standalone library or sidecar service that provides distributed rate limiting (Token Bucket or Leaky Bucket algorithms) for microservices.

Focus: ultra-low latency and handling "thundering herd" problems.

Use Case: For distributed systems and service-oriented architecture (SOA).

📁 `Distributed Rate Limiter/`
---

### 10) Custom Spark SQL Transformer (Spark & Scala/Java): a custom Spark library that performs a complex, non-standard data transformation (like PII masking or advanced currency conversion with historical lookups).

Focus: Optimize the Spark DAG and minimize data shuffling.

Use Case: Contribution to Databricks/Spark infrastructure at a platform level.

📁 `Custom Spark SQL Transformer/`
---

### 11) Observability & Tracing Middleware (Kotlin & OpenTelemetry): Middleware for an HTTP framework (like Ktor or Micronaut) that automatically injects trace IDs and exports metrics to a Prometheus/Grafana stack.

Focus: Developer experience (DX)—how easy is it for another engineer to drop this into their project

Use Case: "Technical Excellence" and "Operations."

📁 `Observability & Tracing Middleware/`
---
### 12) Automated Data Quality Monitor (Python & Snowflake/SQL): tool that runs scheduled "sanity checks" on a dataset (e.g., checking for nulls, outliers, or schema drift) and sends alerts to Slack/PagerDuty.

Focus: Use Great Expectations or a similar framework to define "data contracts."

Use Case: For Data Science and Risk teams who rely on clean, reliable data.

📁 `Automated Data Quality Monitor/`
---
### 13) Multi-Tenant Feature Flag Service (Go or Java): A service that allows teams to toggle features on/off for specific user segments (e.g., "10% of users in California").

Focus: Implement a highly efficient client-side SDK that caches flags to avoid a network hit for every check.

Use Case: Offers built-in flexibility for "Product" Testing and "Operations" roll-out.

📁 `Multi-Tenant Feature Flag Service/`
---
### 14) Financial Ledger with Idempotency (Kotlin): simple ledger service for moving "money" between accounts, ensuring that every request is idempotent (submitting the same transaction twice doesn't double-charge).

Focus: Write-Ahead Log (WAL) or Event Sourcing pattern.

Use Case: For Fintech to avoid duplicate transaction execution.

📁 `Financial Ledger with Idempotency/`
---
### 15)Infrastructure-as-Code (IaC) for a Data Stack (Terraform): a repository that spins up an entire "Block-like" stack: a VPC, a Kafka cluster (via Confluent or Managed), and a Kubernetes cluster.

Focus: Focus on security (IAM roles, VPC peering, and encryption at rest).

Use Case: In the event you need to deploy your own project end-to-end including Infrasctructure deployment.

📁 `Infrastructure-as-Code (IaC)`
---

### 16)Embedding Versioning + Safe Model Upgrades (Shadow Index + Promote/Rollback): A Repo that shows a production-style embedding/index upgrade workflow:
Store documents in a source-of-truth DB (SQLite)**
Build versioned embeddings + a FAISS index for each version (v1, v2, ...)
Run shadow evaluation against a golden query set
Promote the new version if metrics pass, else rollback


Focus: Operational Excellence and Continous Improvement

Use Case: You want to upgrade embeddings (ex: text-embedding-3-small → newer model) to improve relevance.
But embedding upgrades can silently break retrieval, So you can build the new index in shadow, evaluate on a golden set,
only promote if it improves metrics, rollback if it regresses

Why it matters
Prevents production regressions, Enables continuous improvement without downtime

<a href="https://github.com/TeeBee17/engineering-portfolio/tree/main/embedding_versioning">
📁 Embedding Versioning + Safe Model Upgrades
 </a>
---

### 17)Index Freshness + Incremental Updates (CDC + Replay + Lag Monitoring): a This repo demonstrates a production-style pattern:
Source DB (truth) + CDC event log with monotonically increasing offsets
Incremental indexer that consumes CDC and updates an index idempotently
Replay/backfill tooling
Freshness monitoring (lag) + health API

Focus: Real Time updates, reduces potential of stale updates

Use Case: A customer support agent creates a new Case or updates a ticket, and the AI agent needs to “see” it immediately.
Enables real-time use cases like:
“Summarize what happened in the last 10 minutes”
“Find similar incidents right now”

Why it matters: Without incremental updates, AI answers are stale; Full rebuilds are too slow + expensive

<a href="https://github.com/TeeBee17/engineering-portfolio/tree/main/fresh_indexing">
    <img src="https://cdn-icons-png.flaticon.com/512/716/716784.png" width="20" height="20" alt="Folder Icon">
    <b> &nbsp &nbsp Index Freshness + Incremental Updates</b>
  </a>
  <br>
  <br>
  <br>





=============
## Notes
- All projects are built as portfolio examples and do not include proprietary code.
- Where applicable, projects include local Docker setups for reproducibility.

---

## Contact
- LinkedIn: https://www.linkedin.com/in/toyinobakare
- Email: tonyobaker@gmail.com
