from __future__ import annotations

import sys

from pyspark.sql import functions as F
from pyspark.sql import SparkSession


def silver_to_gold(input_prefix: str) -> None:
    spark = SparkSession.builder.appName("wearable-silver-to-gold").getOrCreate()
    silver_path = f"gs://{input_prefix}/silver"
    gold_path = f"gs://{input_prefix}/gold"

    df = spark.read.parquet(silver_path)
    gold = (
        df.withColumn("event_date", F.to_date(F.col("timestamp")))
        .groupBy("event_date")
        .agg(
            F.count("*").alias("events"),
            F.avg(F.col("heart_rate")).alias("avg_heart_rate"),
            F.avg(F.col("steps")).alias("avg_steps"),
        )
    )
    gold.write.mode("overwrite").parquet(gold_path)
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: 02_silver_to_gold.py <bucket-prefix>")
    silver_to_gold(sys.argv[1])

