import logging
from pathlib import Path

import polars as pl

from src.config import RAW_DATA_FILE, SAMPLE_DATA_FILE

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def create_sample_data(raw_path: Path, sample_path: Path, n_rows: int = 100):
    """
    Tự động tạo file sample từ dữ liệu thô nếu chưa có.
    Giúp quy trình chạy mượt mà không cần dùng lệnh terminal bên ngoài.
    """
    if not sample_path.exists():
        logging.info(f"Đang tạo file sample ({n_rows} dòng) tại: {sample_path}")
        # Dùng Lazy API để lấy 100 dòng đầu tiên cực nhanh
        df_sample = pl.scan_ndjson(raw_path).head(n_rows).collect()
        df_sample.write_ndjson(sample_path)


def explore_data(file_path: Path):
    """
    Phân tích dữ liệu bằng Polars Lazy API (Hiệu năng cao nhất).
    """
    try:
        logging.info(f"Đang phân tích dữ liệu (Lazy Mode) từ: {file_path}")

        # Khởi tạo LazyFrame (Chưa đọc dữ liệu vào RAM ngay)
        lf = pl.scan_ndjson(file_path)

        # Thực thi các truy vấn và thu thập kết quả (collect)
        df = lf.collect()

        logging.info("\n========== BÁO CÁO CHẤT LƯỢNG DỮ LIỆU ==========")

        print(f"\n1. Schema:\n{df.collect_schema()}")
        print(f"\n2. Kích thước (Shape):\n{df.shape}")
        print(f"\n3. Null Count:\n{df.null_count()}")
        print(f"\n4. Duplicates:\n{df.is_duplicated().sum()}")

        # Kiểm tra chuỗi rỗng trong context
        empty_context = df.filter(
            pl.col("context").str.strip_chars().str.len_bytes() == 0
        ).height
        print(f"\n5. Empty Contexts: {empty_context}")

        print("\n6. Top Categories:")
        print(df["category"].value_counts(sort=True).head(10))

        logging.info("\n========== HOÀN THÀNH BÁO CÁO ==========")

    except Exception as e:
        logging.error(f" Lỗi trong quá trình phân tích: {e}")
        raise


def main():
    # 1. Tự động kiểm tra và tạo sample nếu chưa có
    if RAW_DATA_FILE.exists():
        create_sample_data(RAW_DATA_FILE, SAMPLE_DATA_FILE)

    # 2. Chạy EDA trên file sample
    if SAMPLE_DATA_FILE.exists():
        explore_data(SAMPLE_DATA_FILE)
    else:
        logging.error(
            "Không tìm thấy dữ liệu để phân tích. Hãy chạy 'uv run ingest' trước."
        )


if __name__ == "__main__":
    main()
