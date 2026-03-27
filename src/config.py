from pathlib import Path

# Cấu hình Dataset nguồn
DATASET_NAME = "databricks/databricks-dolly-15k"

# Cấu hình Đường dẫn thư mục (Sử dụng pathlib cho hiện đại và an toàn)
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


# Tự động tạo thư mục khi import config
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Định nghĩa các file dữ liệu
RAW_DATA_FILE = RAW_DATA_DIR / "dolly_15k.jsonl"
SAMPLE_DATA_FILE = RAW_DATA_DIR / "sample_dolly.jsonl"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "dolly_cleaned.parquet"
