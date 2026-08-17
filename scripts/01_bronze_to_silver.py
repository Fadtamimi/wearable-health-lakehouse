from __future__ import annotations

import sys
from pathlib import Path

from pyspark.sql import functions as F
from pyspark.sql import SparkSession


def bronze_to_silver(input_prefix: str) -> None:
    spark = SparkSession.builder.appName("wearable-bronze-to-silver").getOrCreate()
    bronze_path = f"gs://{input_prefix}/bronze"
    silver_path = f"gs://{input_prefix}/silver"

    df = spark.read.option("header", True).option("inferSchema", True).csv(bronze_path)
    cleaned = (
        df.dropDuplicates()
        .withColumn("ingested_at", F.current_timestamp())
        .withColumn("source_file", F.input_file_name())
    )
    cleaned.write.mode("overwrite").parquet(silver_path)
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: 01_bronze_to_silver.py <bucket-prefix>")
    bronze_to_silver(sys.argv[1])

