from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator


PROJECT_ID = os.getenv("WELLARTH_PROJECT_ID", "wearable-proj-1786637622")
REGION = os.getenv("WELLARTH_REGION", "us-west1")
BUCKET_PREFIX = os.getenv("WELLARTH_BUCKET_PREFIX", "wearable-lakehouse-1786637864")
SERVICE_ACCOUNT = os.getenv(
    "WELLARTH_SERVICE_ACCOUNT",
    "839052457164-compute@developer.gserviceaccount.com",
)

DEFAULT_ARGS = {
    "owner": "copilot",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def build_batch(main_script: str) -> dict:
    return {
        "pyspark_batch": {
            "main_python_file_uri": f"gs://{BUCKET_PREFIX}/scripts/{main_script}",
            "args": [BUCKET_PREFIX],
        },
        "runtime_config": {
            "properties": {
                "spark.driver.cores": "4",
                "spark.executor.cores": "4",
                "spark.executor.instances": "1",
            }
        },
        "environment_config": {
            "execution_config": {"service_account": SERVICE_ACCOUNT}
        },
    }


with DAG(
    dag_id="wearable_health_lakehouse",
    description="Serverless wearable health lakehouse pipeline on GCP",
    start_date=datetime(2026, 8, 16),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
    tags=["wearable", "lakehouse", "serverless", "dataproc"],
) as dag:
    bronze_to_silver = DataprocCreateBatchOperator(
        task_id="bronze_to_silver",
        project_id=PROJECT_ID,
        region=REGION,
        batch=build_batch("01_bronze_to_silver.py"),
        batch_id="bronze-to-silver-{{ ts_nodash | lower }}",
    )

    silver_to_gold = DataprocCreateBatchOperator(
        task_id="silver_to_gold",
        project_id=PROJECT_ID,
        region=REGION,
        batch=build_batch("02_silver_to_gold.py"),
        batch_id="silver-to-gold-{{ ts_nodash | lower }}",
    )

    bronze_to_silver >> silver_to_gold
