# 🚀 LLM Data Engineering Pipeline

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Polars](https://img.shields.io/badge/polars-fast-orange.svg)
![uv](https://img.shields.io/badge/uv-package%20manager-purple.svg)
![Ruff](https://img.shields.io/badge/ruff-linter-red.svg)

## 📋 Tổng quan dự án
Dự án này xây dựng một luồng ETL (Extract, Transform, Load) cục bộ chuẩn Production để thu thập, làm sạch và chuẩn hóa dữ liệu văn bản (`databricks-dolly-15k`), phục vụ cho việc huấn luyện các mô hình Large Language Models (LLMs).

> ** Tiến độ hiện tại:** Hoàn thành Giai đoạn 1 - Thiết lập Framework, Ingestion & EDA.

## 📂 Cấu trúc dự án
```text
llm-data-pipeline/
├── data/                   # (Đã được gitignore)
│   ├── raw/                # Dữ liệu thô (.jsonl)
│   └── processed/          # Dữ liệu sau khi làm sạch (.parquet)
├── src/
│   ├── __init__.py         # Khởi tạo Python package
│   ├── config.py           # Quản lý cấu hình tập trung (Đường dẫn, Dataset)
│   ├── ingest.py           # Script tải dữ liệu từ Hugging Face
│   └── explore.py          # Script phân tích chất lượng dữ liệu (EDA)
├── tests/
│   ├── __init__.py
│   └── test_basic.py       # Unit tests đảm bảo hệ thống ổn định
├── .gitignore              # Bảo vệ dữ liệu và môi trường
├── pyproject.toml          # Quản lý dependency & cấu hình công cụ (Ruff, Pytest)
├── uv.lock                 # Khóa cứng phiên bản thư viện
├── mise.toml               # Khóa cứng phiên bản Python
└── README.md               # Tài liệu dự án
```

## 🛠️ Công nghệ sử dụng
*   **Quản lý Môi trường:** `uv`, `mise`.
*   **Xử lý Dữ liệu:** `polars` (Hiệu năng cực cao), `datasets` (Hugging Face).
*   **Chất lượng Code:** `ruff` (Linter/Formatter), `pytest` (Testing).

## 🚀 Hướng dẫn nhanh (Quick Start)

### 1. Cài đặt môi trường
Đảm bảo bạn đã cài đặt `uv`. Clone repository và chạy các lệnh sau:

```bash
# Đồng bộ môi trường và cài đặt thư viện
uv sync
```

```bash
# Kích hoạt môi trường ảo
source .venv/bin/activate
```

### 2. Thực thi Pipeline

```bash
# Bước 1: Tải dữ liệu thô (15.000 dòng) từ Hugging Face
PYTHONPATH=. python src/ingest.py
```

```bash
# Bước 2: Tạo mẫu nhỏ để test (Chạy lệnh này trong terminal)
head -n 100 data/raw/dolly_15k.jsonl > data/raw/sample_dolly.jsonl
```

```bash
# Bước 3: Phân tích dữ liệu (EDA)
PYTHONPATH=. python src/explore.py
```

### 3. Kiểm tra chất lượng (Quality Control)

```bash
# Kiểm tra lỗi code bằng Ruff
uv run ruff check .
```

```bash
# Chạy Unit Tests
uv run pytest
```

---
*Dự án đang trong quá trình phát triển. Các bước Transform dữ liệu sẽ được cập nhật sớm.*
