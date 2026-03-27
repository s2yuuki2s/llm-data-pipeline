import logging
from pathlib import Path

import polars as pl

from src.config import RAW_DATA_FILE, SAMPLE_DATA_FILE

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def create_sample_data(raw_path: Path, sample_path: Path, n_rows: int = 100):
    """
    Automatically create a sample file from raw data if it doesn't exist.
    Ensures a smooth workflow without requiring external terminal commands.
    """
    if not sample_path.exists():
        logging.info(f"Creating sample file ({n_rows} rows) at: {sample_path}")
        # Use Lazy API to fetch the first 100 rows very quickly
        df_sample = pl.scan_ndjson(raw_path).head(n_rows).collect()
        df_sample.write_ndjson(sample_path)


def explore_data(file_path: Path):
    """
    Analyze data using Polars Lazy API (Highest performance).
    """
    try:
        logging.info(f"Analyzing data (Lazy Mode) from: {file_path}")

        # Initialize LazyFrame (Data not read into RAM immediately)
        lf = pl.scan_ndjson(file_path)

        # Execute queries and collect results
        df = lf.collect()

        logging.info("\n========== DATA QUALITY REPORT ==========")

        print(f"\n1. Schema:\n{df.collect_schema()}")
        print(f"\n2. Shape:\n{df.shape}")
        print(f"\n3. Null Count:\n{df.null_count()}")
        print(f"\n4. Duplicates:\n{df.is_duplicated().sum()}")

        # Check for empty strings in context
        empty_context = df.filter(
            pl.col("context").str.strip_chars().str.len_bytes() == 0
        ).height
        print(f"\n5. Empty Contexts: {empty_context}")

        print("\n6. Top Categories:")
        print(df["category"].value_counts(sort=True).head(10))

        logging.info("\n========== REPORT COMPLETE ==========")

    except Exception as e:
        logging.error(f" Error during analysis: {e}")
        raise


def main():
    # 1. Automatically check and create sample if it doesn't exist
    if RAW_DATA_FILE.exists():
        create_sample_data(RAW_DATA_FILE, SAMPLE_DATA_FILE)

    # 2. Run EDA on the sample file
    if SAMPLE_DATA_FILE.exists():
        explore_data(SAMPLE_DATA_FILE)
    else:
        logging.error(
            "Data not found for analysis. Please run 'uv run python -m src.ingest' first."
        )


if __name__ == "__main__":
    main()
