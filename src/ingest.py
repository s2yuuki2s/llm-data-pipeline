"""
Data Ingestion Module
=====================
Handles downloading and local storage of LLM training datasets from Hugging Face.
"""

import logging
from pathlib import Path
from datasets import load_dataset
from src.config import RAW_DATA_FILE, DATASET_NAME

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_dataset(dataset_name: str, output_path: Path):
    """
    Downloads Dolly-15k dataset from Hugging Face and saves as JSONL.
    """
    try:
        logging.info(f"Extracting dataset: {dataset_name}")

        # Load dataset from Hugging Face
        dataset = load_dataset(dataset_name, split="train")

        # Ensure raw data directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save to local JSONL (standard format for LLM training data)
        dataset.to_json(output_path)

        logging.info(
            f"Successfully ingested {len(dataset)} records to {output_path}"
        )

    except Exception as e:
        logging.error(f"Failed to ingest dataset: {e}")
        raise


if __name__ == "__main__":
    download_dataset(DATASET_NAME, RAW_DATA_FILE)
