import logging
from datasets import load_dataset
from src.config import DATASET_NAME, RAW_DATA_FILE

# Thiết lập Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ingest_data(dataset_name: str, output_path: str):
    """
    Hàm kết nối API, tải dữ liệu và lưu xuống ổ cứng.
    """
    try:
        logging.info(f"Bắt đầu tải dataset: {dataset_name} (chỉ lấy tập train)")

        # Gọi hàm tải dữ liệu
        dataset = load_dataset(dataset_name, split="train")

        logging.info("Đã tải xong dữ liệu vào bộ nhớ. Đang tiến hành lưu ra file...")

        # Lưu dataset ra file JSON Lines.
        dataset.to_json(output_path, force_ascii=False)

        logging.info(f" Thành công! Dữ liệu đã được lưu tại: {output_path}")

    except Exception as e:
        logging.error(f" Quá trình tải dữ liệu thất bại: {e}")
        raise


def main():
    # Sử dụng cấu hình từ config.py
    ingest_data(DATASET_NAME, RAW_DATA_FILE)


if __name__ == "__main__":
    main()
