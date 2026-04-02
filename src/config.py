from pathlib import Path

# Dataset Source: Dolly-15k from Databricks
DATASET_NAME = "databricks/databricks-dolly-15k"

# Directory Path Configuration
# Utilizes pathlib for cross-platform compatibility
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


# Initialize data directories on import
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# File Path Assets
RAW_DATA_FILE = RAW_DATA_DIR / "dolly_15k.jsonl"
SAMPLE_DATA_FILE = RAW_DATA_DIR / "sample_dolly.jsonl"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "dolly_cleaned.parquet"
