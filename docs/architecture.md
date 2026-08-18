# Architecture

```text
Wearable source data
        |
        v
Cloud Storage bronze
        |
        v
Dataproc Serverless bronze -> silver
        |
        v
Cloud Storage silver
        |
        v
Dataproc Serverless silver -> gold
        |
        v
Cloud Storage gold / BigQuery
```

## Notes

- Keep credentials in Secret Manager.
- Use least-privilege IAM for the Dataproc service account.
- Prefer managed services only; no self-managed clusters.
- Load the gold layer into BigQuery with an Airflow-managed load job.
