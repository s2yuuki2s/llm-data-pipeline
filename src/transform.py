"""
PySpark ETL Pipeline for LLM Instruction Data
==============================================
This module implements a modular ETL pipeline for cleansing and enriching
Dolly-15k datasets for production LLM fine-tuning.
"""

import json
import logging
from pathlib import Path
from datetime import datetime

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType

from src.config import PROCESSED_DATA_FILE, RAW_DATA_FILE

# Logging Setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_spark_session(app_name: str = "LLM_Data_Pipeline") -> SparkSession:
    """Initialize a SparkSession with optimized configs."""
    spark = (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.adaptive.enabled", "true")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    logging.info(f"✓ Created SparkSession: {app_name}")
    return spark


def get_dolly_schema() -> StructType:
    """Define structural contract for the Dolly-15k dataset."""
    return StructType(
        [
            StructField("instruction", StringType(), nullable=False),
            StructField("context", StringType(), nullable=True),
            StructField("response", StringType(), nullable=False),
            StructField("category", StringType(), nullable=True),
        ]
    )


def load_raw_data(spark: SparkSession, input_path: Path) -> DataFrame:
    """Read raw JSONL data with enforced schema."""
    logging.info(f"Extracting raw data: {input_path}")
    return spark.read.format("json").schema(get_dolly_schema()).load(str(input_path))


def clean_data(df: DataFrame) -> DataFrame:
    """
    Apply core data cleansing:
    - Normalizes null/empty contexts.
    - Trims whitespace across text fields.
    - Removes exact record duplicates.
    """
    logging.info("Transform Stage 1: Cleansing...")
    
    # Standardize null/empty contexts to empty strings
    df_clean = df.withColumn(
        "context",
        F.when(
            (F.col("context").isNull()) | (F.trim(F.col("context")) == ""),
            F.lit(""),
        ).otherwise(F.trim(F.col("context"))),
    )

    # Normalize whitespace for key text fields
    text_cols = ["instruction", "response"]
    for col in text_cols:
        df_clean = df_clean.withColumn(
            col, F.trim(F.regexp_replace(F.col(col), r"\s+", " "))
        )

    # De-duplicate records
    return df_clean.dropDuplicates()


def enrich_data(df: DataFrame) -> DataFrame:
    """
    Enriches dataset with linguistic metadata and training-ready fields.
    """
    logging.info("Transform Stage 2: Enrichment...")
    return (
        df.withColumn("instruction_length", F.length(F.col("instruction")))
        .withColumn("response_length", F.length(F.col("response")))
        .withColumn("has_context", (F.col("context") != "").cast("boolean"))
        .withColumn("word_count", F.size(F.split(F.col("response"), r"\s+")))
        .withColumn("processing_timestamp", F.current_timestamp())
        # Generate formatted instruction field for downstream training
        .withColumn(
            "combined_text",
            F.concat_ws(
                "\n\n",
                F.lit("Instruction: "), F.col("instruction"),
                F.when(F.col("has_context"), F.concat(F.lit("\nContext: "), F.col("context"))).otherwise(F.lit("")),
                F.lit("\nResponse: "), F.col("response"),
            ),
        )
    )


def filter_data(df: DataFrame) -> DataFrame:
    """
    Filters records based on heuristic quality thresholds.
    """
    logging.info("Transform Stage 3: Quality filtering...")
    return df.filter(
        (F.col("instruction_length") > 5)
        & (F.col("response_length") > 10)
        & (F.col("instruction").isNotNull())
        & (F.col("response").isNotNull())
    )


def compute_audit_log(spark: SparkSession, df: DataFrame) -> dict:
    """
    Utilizes Spark SQL to generate an audit report for data lineage tracking.
    """
    logging.info("Transform Stage 4: Executing SQL-based audit...")
    df.createOrReplaceTempView("transformed_data")
    
    summary = spark.sql("""
        SELECT 
            COUNT(*) as total_records,
            AVG(instruction_length) as avg_instruction_len,
            AVG(response_length) as avg_response_len,
            COUNT(DISTINCT category) as unique_categories
        FROM transformed_data
    """).collect()[0]

    return {
        "total_records": summary["total_records"],
        "avg_instruction_len": round(summary["avg_instruction_len"], 2),
        "avg_response_len": round(summary["avg_response_len"], 2),
        "unique_categories": summary["unique_categories"],
        "timestamp": datetime.now().isoformat()
    }


def save_processed_data(df: DataFrame, output_path: Path):
    """
    Saves transformed data in partitioned Parquet format.
    Optimizes storage and query performance via category-based partitioning.
    """
    logging.info(f"Loading data into sink: {output_path} (Partitioned by Category)")
    
    (
        df.write.mode("overwrite")
        .partitionBy("category")
        .format("parquet")
        .save(str(output_path))
    )
    logging.info("✓ Data successfully loaded to sink.")


def main():
    spark = None
    try:
        spark = create_spark_session()
        
        if not RAW_DATA_FILE.exists():
            logging.error(f"❌ Input missing at {RAW_DATA_FILE}")
            return

        # Pipeline Orchestration
        df_raw = load_raw_data(spark, RAW_DATA_FILE)
        
        df_clean = clean_data(df_raw)
        df_enriched = enrich_data(df_clean)
        df_final = filter_data(df_enriched)
        
        # Sink Data (Partitioned Parquet)
        save_processed_data(df_final, PROCESSED_DATA_FILE)
        
        # Data Quality Audit
        audit_logs = compute_audit_log(spark, df_final)
        
        # Persist audit findings for monitoring
        audit_path = PROCESSED_DATA_FILE.parent / "audit_log.json"
        with open(audit_path, "w") as f:
            json.dump(audit_logs, f, indent=4)
        
        logging.info(f"📊 Pipeline Success: {audit_logs}")

    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}")
        raise
    finally:
        if spark:
            spark.stop()
            logging.info("🛑 SparkSession terminated.")


if __name__ == "__main__":
    main()
