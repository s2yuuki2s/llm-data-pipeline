import os
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

def test_config_paths():
    """
    Kiểm tra xem các thư mục dữ liệu có tồn tại không.
    """
    assert os.path.exists(RAW_DATA_DIR)
    assert os.path.exists(PROCESSED_DATA_DIR)

def test_file_naming():
    """
    Kiểm tra định dạng file dữ liệu.
    """
    from src.config import RAW_DATA_FILE
    assert RAW_DATA_FILE.endswith(".jsonl")
