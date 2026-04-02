from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR, RAW_DATA_FILE


def test_config_paths():
    """
    Verify that data directories are initialized correctly.
    """
    assert RAW_DATA_DIR.exists()
    assert PROCESSED_DATA_DIR.exists()


def test_file_naming_conventions():
    """
    Ensure input data adheres to the expected JSONL format.
    """
    assert RAW_DATA_FILE.suffix == ".jsonl"
    assert "dolly" in RAW_DATA_FILE.name.lower()
