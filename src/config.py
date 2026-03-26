import os

# Cấu hình Dataset nguồn
DATASET_NAME = "databricks/databricks-dolly-15k"

# Cấu hình Đường dẫn thư mục
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

# Đảm bảo thư mục tồn tại khi import config
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Tên file dữ liệu
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, "dolly_15k.jsonl")
SAMPLE_DATA_FILE = os.path.join(RAW_DATA_DIR, "sample_dolly.jsonl")
PROCESSED_DATA_FILE = os.path.join(PROCESSED_DATA_DIR, "dolly_cleaned.parquet")
