import polars as pl
import logging
from src.config import SAMPLE_DATA_FILE

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def explore_data(file_path: str):
    """
    Hàm đọc và phân tích dữ liệu thô bằng Polars để chuẩn bị cho bước làm sạch.
    """
    try:
        logging.info(f"Đang đọc dữ liệu từ: {file_path}")

        # Đọc file NDJSON bằng Polars
        df = pl.read_ndjson(file_path)

        logging.info("\n========== BÁO CÁO CHẤT LƯỢNG DỮ LIỆU ==========")

        # In ra Schema (Tên cột & Kiểu dữ liệu)
        print("\n1. Cấu trúc dữ liệu (Schema):")
        print(df.collect_schema())

        # In ra kích thước DataFrame (Dòng, Cột)
        print("\n2. Kích thước (Shape):")
        print(df.shape)

        # Kiểm tra Null
        print("\n3. Số lượng dòng chứa giá trị Null ở mỗi cột:")
        print(df.null_count())

        # Đếm tổng số dòng bị trùng lặp hoàn toàn
        print("\n4. Số lượng dòng dữ liệu trùng lặp (Duplicates):")
        print(df.is_duplicated().sum())

        # Kiểm tra "chuỗi rỗng" trong cột 'context'
        print("\n5. Số lượng dòng có 'context' là chuỗi rỗng:")
        empty_context = df.filter(
            pl.col("context").str.strip_chars().str.len_bytes() == 0
        ).height
        print(empty_context)

        # Thống kê các thể loại câu hỏi
        print("\n6. Phân phối các thể loại (Categories):")
        print(df["category"].value_counts(sort=True))

        logging.info("\n========== HOÀN THÀNH BÁO CÁO ==========")

    except Exception as e:
        logging.error(f" Lỗi trong quá trình phân tích: {e}")
        raise


def main():
    # Sử dụng cấu hình từ config.py
    explore_data(SAMPLE_DATA_FILE)


if __name__ == "__main__":
    main()
