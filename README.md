# LLM Data Pipeline

Dự án này là một pipeline ETL đơn giản để xử lý dữ liệu từ Hugging Face (dataset Dolly-15k) phục vụ việc chuẩn bị dữ liệu cho LLM.

## Cấu trúc thư mục
- `data/`: Chứa dữ liệu thô (raw) và dữ liệu sau khi xử lý (processed).
- `src/`: Mã nguồn chính của dự án.
  - `config.py`: Quản lý đường dẫn và các tham số cấu hình.
  - `ingest.py`: Tải dữ liệu từ Hugging Face và lưu xuống local.
  - `explore.py`: Phân tích nhanh dữ liệu (EDA) sử dụng Polars.
- `tests/`: Các script kiểm tra cơ bản.
- `pyproject.toml`: Khai báo thư viện và cấu hình `uv`.

## Cài đặt
Yêu cầu máy đã cài sẵn `uv`.

```bash
uv sync
```

## Cách chạy

### 1. Tải dữ liệu
Lệnh này sẽ tải dataset `databricks-dolly-15k` về thư mục `data/raw/`.

```bash
uv run python -m src.ingest
```

### 2. Phân tích dữ liệu
Sử dụng Polars để kiểm tra cấu trúc dữ liệu và các thông số cơ bản.

```bash
uv run python -m src.explore
```

### 3. Kiểm tra code
Chạy linter và unit tests để đảm bảo code không có lỗi cú pháp hoặc logic cơ bản.

```bash
uv run ruff check .
uv run pytest
```
