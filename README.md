# Engineering Portfolio (10+ Years)

This repository is a curated collection of engineering, streaming, analytics, and distributed systems projects I’ve built over the last 10+ years.

The focus of this portfolio is on:
- scalable data pipelines (batch + streaming)
- distributed systems and platform thinking
- data modeling and analytics enablement
- experimentation and metric reliability
- production-grade engineering practices (testing, observability, documentation)

---

## Projects

### 1) Member Messaging Feature Store (Flink + Kafka)
**Tech:** Apache Flink, Kafka (MSK-compatible), Java, Docker  
A real-time feature store that merges recent user activity and messaging history to generate unified per-member messaging features for eligibility, suppression, dashboards, and experimentation.

📁 `member-messaging-feature-store/`

---

### 2) Experimentation Metrics Framework
**Tech:** Spark, SQL, Python  
Reusable metrics pipeline for A/B testing with standardized exposure/outcome modeling and metric definitions.

📁 `experimentation-metrics-framework/`

---

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

### 6) High-Throughput Event Aggregator (Kafka & Kotlin): a service that consumes a high-volume stream of "transaction" events from Kafka and aggregates them into time-series windows (e.g., total spend per category every minute).

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

---

### 9) Distributed Rate Limiter (Java & Redis): standalone library or sidecar service that provides distributed rate limiting (Token Bucket or Leaky Bucket algorithms) for microservices.

Focus: ultra-low latency and handling "thundering herd" problems.

Use Case: For distributed systems and service-oriented architecture (SOA).

---

### 10) Custom Spark SQL Transformer (Spark & Scala/Java): a custom Spark library that performs a complex, non-standard data transformation (like PII masking or advanced currency conversion with historical lookups).

Focus: Optimize the Spark DAG and minimize data shuffling.

Use Case: Contribution to Databricks/Spark infrastructure at a platform level.

### 11) Observability & Tracing Middleware (Kotlin & OpenTelemetry): Middleware for an HTTP framework (like Ktor or Micronaut) that automatically injects trace IDs and exports metrics to a Prometheus/Grafana stack.

Focus: Developer experience (DX)—how easy is it for another engineer to drop this into their project

Use Case: "Technical Excellence" and "Operations."

### 12) Automated Data Quality Monitor (Python & Snowflake/SQL): tool that runs scheduled "sanity checks" on a dataset (e.g., checking for nulls, outliers, or schema drift) and sends alerts to Slack/PagerDuty.

Focus: Use Great Expectations or a similar framework to define "data contracts."

Use Case: For Data Science and Risk teams who rely on clean, reliable data.

### 13) Multi-Tenant Feature Flag Service (Go or Java): A service that allows teams to toggle features on/off for specific user segments (e.g., "10% of users in California").

Focus: Implement a highly efficient client-side SDK that caches flags to avoid a network hit for every check.

Use Case: Offers built-in flexibility for "Product" Testing and "Operations" roll-out.

### 14) Financial Ledger with Idempotency (Kotlin): simple ledger service for moving "money" between accounts, ensuring that every request is idempotent (submitting the same transaction twice doesn't double-charge).

Focus: Write-Ahead Log (WAL) or Event Sourcing pattern.

Use Case: For Fintech to avoid duplicate transaction execution.

### 15)Infrastructure-as-Code (IaC) for a Data Stack (Terraform): a repository that spins up an entire "Block-like" stack: a VPC, a Kafka cluster (via Confluent or Managed), and a Kubernetes cluster.

Focus: Focus on security (IAM roles, VPC peering, and encryption at rest).

Use Case: In the event you need to deploy your own project end-to-end including Infrasctructure deployment.



=============
## Notes
- All projects are built as portfolio examples and do not include proprietary code.
- Where applicable, projects include local Docker setups for reproducibility.

---

## Contact
- LinkedIn: https://www.linkedin.com/in/toyinobakare
- Email: tonyobaker@gmail.com
