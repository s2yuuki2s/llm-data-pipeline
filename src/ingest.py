import os
import logging
from datasets import load_dataset

# Thiết lập hệ thống Logging chuẩn
# Điều này giúp in ra màn hình thời gian chạy và phân loại thông báo (INFO, ERROR)
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
    # Tạo thư mục nếu chưa có
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)

    # Khai báo đường dẫn lưu file
    output_file = os.path.join(output_dir, "dolly_15k.jsonl")

    # Gọi hàm thực thi
    ingest_data("databricks/databricks-dolly-15k", output_file)


if __name__ == "__main__":
    main()
