import logging
from pathlib import Path

from datasets import load_dataset

from src.config import DATASET_NAME, RAW_DATA_FILE

# Logging Setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ingest_data(dataset_name: str, output_path: Path, force_download: bool = False):
    """
    Download data from Hugging Face and save it to disk.
    If the file exists, skip downloading to save time (unless force_download=True).
    """
    if output_path.exists() and not force_download:
        logging.info(f"Data already exists at {output_path}. Skipping download.")
        return

    try:
        logging.info(f"Starting to download dataset: {dataset_name} (train set only)")

        # Download data
        dataset = load_dataset(dataset_name, split="train")

        logging.info("Download complete. Proceeding to save to file...")

        # Save dataset to JSON Lines file.
        dataset.to_json(output_path)

        logging.info(f" Success! Data saved at: {output_path}")

    except Exception as e:
        logging.error(f" Data ingestion process failed: {e}")
        raise


def main():
    ingest_data(DATASET_NAME, RAW_DATA_FILE)


if __name__ == "__main__":
    main()
