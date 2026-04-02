"""
EDA Module (Exploratory Data Analysis)
=====================================
Leverages Polars Lazy API for ultra-fast profiling of raw datasets.
"""

import logging
from pathlib import Path
import polars as pl
from src.config import RAW_DATA_FILE, SAMPLE_DATA_FILE

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def profile_raw_data(file_path: Path):
    """
    Analyzes raw JSONL data using Polars for high-performance profiling.
    """
    try:
        logging.info(f"Scanning raw dataset (Lazy Mode): {file_path}")

        # Scan as LazyFrame (won't load to RAM until 'collect' is called)
        lf = pl.scan_ndjson(file_path)
        df = lf.collect()

        logging.info("--- Data Quality Report ---")

        # 1. Basic Stats
        print(f"\n1. Schema:\n{df.collect_schema()}")
        print(f"\n2. Dimensions:\nRows: {df.height:,}, Columns: {df.width}")

        # 2. Null Analysis
        null_stats = df.null_count()
        print(f"\n3. Null Values:\n{null_stats}")

        # 3. Duplicate Detection
        dup_count = df.is_duplicated().sum()
        print(f"\n4. Duplicate Rows: {dup_count:,}")

        # 4. Context Empty Analysis (LLM specific)
        empty_context = df.filter(
            pl.col("context").str.strip_chars().str.len_bytes() == 0
        ).height
        print(f"\n5. Empty/Whitespace Contexts: {empty_context:,}")

        # 5. Category Distribution
        print("\n6. Category Distribution (Top 10):")
        print(df["category"].value_counts(sort=True).head(10))

        logging.info("Profiling complete.")

    except Exception as e:
        logging.error(f"Error during EDA: {e}")
        raise


def create_sample(raw_path: Path, sample_path: Path, n_rows: int = 100):
    """Generates a smaller sample file for rapid testing."""
    if not sample_path.exists():
        logging.info(f"Creating sample file ({n_rows} rows) at {sample_path}")
        df_sample = pl.scan_ndjson(raw_path).head(n_rows).collect()
        df_sample.write_ndjson(sample_path)


def main():
    if RAW_DATA_FILE.exists():
        create_sample(RAW_DATA_FILE, SAMPLE_DATA_FILE)
        profile_raw_data(RAW_DATA_FILE)
    else:
        logging.error("Raw data file not found. Run ingestion first.")


if __name__ == "__main__":
    main()
