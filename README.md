# 🚀 LLM Data Engineering Pipeline

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Polars](https://img.shields.io/badge/polars-fast-orange.svg)
![uv](https://img.shields.io/badge/uv-package%20manager-purple.svg)

## Tổng quan dự án
Dự án này xây dựng một luồng ETL (Extract, Transform, Load) cục bộ chuẩn Production để thu thập, làm sạch và chuẩn hóa dữ liệu văn bản (`databricks-dolly-15k`), phục vụ cho việc huấn luyện các mô hình Large Language Models (LLMs).

> ** Tiến độ hiện tại:** Hoàn thành Giai đoạn 1 - Data Ingestion (Thu thập) & EDA (Phân tích khám phá).

## Cấu trúc dự án
llm-data-pipeline/
├── data/                   # (Đã được gitignore để bảo mật)
│   ├── raw/                # Chứa dữ liệu thô tải về (.jsonl)
│   └── processed/          # Chứa dữ liệu sau khi làm sạch (Parquet)
├── src/
│   ├── ingest.py           # Script kết nối API Hugging Face tải data
│   └── explore.py          # Script dùng Polars nội soi chất lượng data
├── .gitignore              # Tấm khiên bảo vệ data và môi trường
├── pyproject.toml          # Quản lý dependency của dự án
├── mise.toml               # Khóa cứng phiên bản Python (3.11)
└── README.md               # Tài liệu dự án

## Công nghệ sử dụng (Tech Stack)
* **Quản lý Môi trường & Package:** `mise`, `uv`.
* **Data Extraction:** `datasets` (Hugging Face API).
* **Data Profiling (EDA):** `polars` (Xử lý dữ liệu tốc độ cao bằng lõi Rust).
* **Hệ điều hành:** Windows 11 với WSL2.

## Hướng dẫn cài đặt và chạy code (Dành cho Ngày 1)

**1. Khởi tạo môi trường**
Clone repository này về máy và thiết lập môi trường ảo:
> uv sync
> source .venv/bin/activate

**2. Thực thi Pipeline**
Chạy tuần tự các lệnh sau để tự động hóa việc lấy dữ liệu và phân tích:

> # Bước 1: Tải dữ liệu thô (15.000 dòng) từ Hugging Face
> python src/ingest.py
> 
> # Bước 2: Tạo một file sample nhỏ (100 dòng) để test nhanh hệ thống
> head -n 100 data/raw/dolly_15k.jsonl > data/raw/sample_dolly.jsonl
> 
> # Bước 3: Chạy kịch bản phân tích EDA để tìm lỗi dữ liệu
> python src/explore.py
