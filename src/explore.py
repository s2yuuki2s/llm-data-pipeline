import polars as pl
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def explore_data(file_path: str):
    """
    Hàm đọc và phân tích dữ liệu thô bằng Polars để chuẩn bị cho bước làm sạch.
    """
    try:
        logging.info(f"Đang đọc dữ liệu từ: {file_path}")

        # TODO 1: Đọc file NDJSON bằng Polars
        df = pl.read_ndjson(file_path)

        logging.info("\n========== BÁO CÁO CHẤT LƯỢNG DỮ LIỆU ==========")

        # TODO 2: In ra Schema (Tên cột & Kiểu dữ liệu)
        print("\n1. Cấu trúc dữ liệu (Schema):")
        print(df.collect_schema())

        # TODO 3: In ra kích thước DataFrame (Dòng, Cột)
        print("\n2. Kích thước (Shape):")
        print(df.shape)

        # TODO 4: Kiểm tra Null
        print("\n3. Số lượng dòng chứa giá trị Null ở mỗi cột:")
        print(df.null_count())

        # TODO 5: Đếm tổng số dòng bị trùng lặp hoàn toàn
        # Gợi ý: Tìm hiểu phương thức df.is_duplicated().sum()
        print("\n4. Số lượng dòng dữ liệu trùng lặp (Duplicates):")
        print(df.is_duplicated().sum())

        # TODO 6: Kiểm tra "chuỗi rỗng" trong cột 'context'
        # Đôi khi context không Null nhưng lại là khoảng trắng ("" hoặc "   ").
        # Gợi ý: Lọc (filter) cột 'context' dựa trên độ dài chuỗi (str.len_bytes() == 0)
        print("\n5. Số lượng dòng có 'context' là chuỗi rỗng:")
        empty_context = df.filter(
            pl.col("context").str.strip_chars().str.len_bytes() == 0
        ).height
        print(empty_context)

        # TODO 7: Thống kê các thể loại câu hỏi
        # Gợi ý: Tìm hàm đếm tần suất xuất hiện của các giá trị trong cột 'category' (value_counts)
        print("\n6. Phân phối các thể loại (Categories):")
        print(df["category"].value_counts(sort=True))

        logging.info("\n========== HOÀN THÀNH BÁO CÁO ==========")

    except Exception as e:
        logging.error(f"❌ Lỗi trong quá trình phân tích: {e}")
        raise


def main():
    # Mẹo: Lúc code TODO, bạn có thể truyền "data/raw/sample_dolly.jsonl" để chạy cho nhanh.
    # Khi code chuẩn rồi thì mới đổi lại thành file 15k dòng bên dưới.
    file_path = "data/raw/sample_dolly.jsonl"
    explore_data(file_path)


if __name__ == "__main__":
    main()
