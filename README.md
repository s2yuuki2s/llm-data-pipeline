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
│   ├── __init__.py         # Biến src thành Python package
│   ├── config.py           # Quản lý cấu hình tập trung
│   ├── ingest.py           # Logic tải dữ liệu
│   └── explore.py          # Logic phân tích (EDA)
├── tests/
│   ├── __init__.py
│   └── test_basic.py       # Unit tests
├── pyproject.toml          # Cấu hình dự án & Script Entry Points
└── README.md
```

## 🚀 Hướng dẫn nhanh (Quick Start)

### 1. Cài đặt môi trường
Đảm bảo bạn đã cài đặt `uv`. Chạy lệnh sau để đồng bộ mọi thứ:

```bash
uv sync
```

### 2. Thực thi Pipeline (Sử dụng lệnh tắt)
Nhờ cấu hình `project.scripts` trong `pyproject.toml`, bạn có thể chạy các lệnh này ở bất cứ đâu trong dự án mà không lo về đường dẫn:

```bash
# Bước 1: Tải dữ liệu thô từ Hugging Face
uv run ingest
```

```bash
# Bước 2: Tạo mẫu 100 dòng để test nhanh
head -n 100 data/raw/dolly_15k.jsonl > data/raw/sample_dolly.jsonl
```

```bash
# Bước 3: Phân tích dữ liệu (EDA)
uv run explore
```

### 3. Kiểm tra chất lượng (Quality Control)

```bash
# Kiểm tra lỗi code bằng Ruff
uv run ruff check .

# Chạy Unit Tests
uv run pytest
```

---
*Dự án hiện tại được cấu hình theo chuẩn Python Package hiện đại.*
