# Wearable Health Lakehouse

Serverless GCP lakehouse for wearable health data.

## Stack

- Cloud Storage for bronze, silver, and gold zones
- Cloud Composer / Airflow for orchestration
- Dataproc Serverless for Spark transforms
- BigQuery for the final analytics layer
- Secret Manager, Cloud Logging, and Cloud Monitoring for operations

## Project layout

- `dags/` - Airflow DAGs
- `scripts/` - Dataproc Serverless Spark jobs
- `docs/` - architecture and implementation notes
- `infra/` - IaC placeholders
- `tests/` - smoke tests

## Pipeline

1. Bronze data lands in Cloud Storage.
2. Dataproc Serverless transforms bronze to silver.
3. Dataproc Serverless transforms silver to gold.
4. Gold is published for analytics in BigQuery or curated GCS output.

## Screenshots to capture

- DAG graph with both tasks successful
- Dataproc Serverless batch details for each job
- Cloud Storage bucket showing `bronze/`, `silver/`, `gold/`, and `scripts/`
- BigQuery table preview for the gold layer
- Cloud Logging entry for a successful pipeline run
- This README section and the architecture diagram

