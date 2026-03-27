from pathlib import Path

# Source Dataset Configuration
DATASET_NAME = "databricks/databricks-dolly-15k"

# Directory Path Configuration (Using pathlib for modern and safe path handling)
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


# Automatically create directories when config is imported
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Data File Definitions
RAW_DATA_FILE = RAW_DATA_DIR / "dolly_15k.jsonl"
SAMPLE_DATA_FILE = RAW_DATA_DIR / "sample_dolly.jsonl"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "dolly_cleaned.parquet"
