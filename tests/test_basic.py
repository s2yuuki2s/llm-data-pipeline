import os

from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR


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
    assert RAW_DATA_FILE.name.endswith(".jsonl")
