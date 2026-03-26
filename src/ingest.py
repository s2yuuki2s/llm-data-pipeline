import logging
from pathlib import Path

from datasets import load_dataset

from src.config import DATASET_NAME, RAW_DATA_FILE

# Thiết lập Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ingest_data(dataset_name: str, output_path: Path, force_download: bool = False):
    """
    Tải dữ liệu từ Hugging Face và lưu xuống ổ cứng.
    Nếu file đã tồn tại, bỏ qua bước tải để tiết kiệm thời gian
    (trừ khi force_download=True).
    """
    if output_path.exists() and not force_download:
        logging.info(f"Dữ liệu đã tồn tại tại {output_path}. Bỏ qua bước tải.")
        return

    try:
        logging.info(f"Bắt đầu tải dataset: {dataset_name} (chỉ lấy tập train)")

        # Tải dữ liệu
        dataset = load_dataset(dataset_name, split="train")

        logging.info("Đã tải xong. Đang tiến hành lưu ra file...")

        # Lưu dataset ra file JSON Lines.
        dataset.to_json(output_path, force_ascii=False)

        logging.info(f" Thành công! Dữ liệu đã được lưu tại: {output_path}")

    except Exception as e:
        logging.error(f" Quá trình tải dữ liệu thất bại: {e}")
        raise


def main():
    ingest_data(DATASET_NAME, RAW_DATA_FILE)


if __name__ == "__main__":
    main()
