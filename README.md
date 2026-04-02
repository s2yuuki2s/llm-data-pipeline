# LLM Data ETL Pipeline (PySpark)

A production-ready ETL pipeline designed for processing and cleaning LLM
instruction tuning datasets (Dolly-15k). This project demonstrates modern Data
Engineering practices including distributed processing with PySpark, data
partitioning, and containerization.

---

## 🛠️ Architecture & Tech Stack

- **PySpark 3.5+**: Core engine for distributed data transformation and
  SQL-based auditing.
- **Polars**: Leveraged for high-performance Exploratory Data Analysis (EDA).
- **Hugging Face Datasets**: Source of raw instruction data.
- **uv**: Modern, ultra-fast Python package and environment manager.
- **Docker**: Containerized environment ensuring reproducibility
  (Java 17 + Python 3.11).
- **Pytest**: Comprehensive unit testing for transformation logic.

---

## 🚀 Execution Guide

### 1. Using Docker (Recommended)

The simplest way to run the pipeline without installing Java or Spark locally:

```bash
docker build -t llm-pipeline .
docker run -it llm-pipeline
```

### 2. Local Execution

Ensure you have **Python 3.11+** and **Java 17+** installed.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment and install dependencies
uv sync

# Run the full pipeline
chmod +x run_pipeline.sh
./run_pipeline.sh
```

---

## 🔄 ETL Pipeline Stages

1. **Extract**: Ingests JSONL data from Hugging Face repository into local
   storage.
2. **Explore (EDA)**: Fast profiling using Polars to identify data quality
   issues (duplicates, nulls).
3. **Transform (PySpark)**:
    - **Clean**: Normalizes whitespace, handles null contexts, and removes
      exact duplicates.
    - **Enrich**: Computes token-level metadata (instruction/response lengths,
      word counts).
    - **Filter**: Enforces quality thresholds for training-ready data.
4. **Load**: Saves the final dataset in **Parquet** format, partitioned by
   `category` for optimized downstream querying.
5. **Audit**: Generates an `audit_log.json` containing pipeline performance
   metrics using Spark SQL.

---

## 🧪 Quality Assurance

We maintain comprehensive unit test coverage for core transformation logic.

```bash
uv run pytest tests/ -v
```

---

## 📂 Project Structure

```text
llm-data-pipeline/
├── src/
│   ├── transform.py     # Main PySpark ETL (Modular + Spark SQL)
│   ├── ingest.py        # Data ingestion logic
│   ├── explore.py       # EDA with Polars
│   └── config.py        # Environment & Path configuration
├── tests/               # Unit tests for transformations
├── data/                # Data storage (Raw & Processed Parquet)
├── Dockerfile           # Container definition
├── run_pipeline.sh      # Orchestration script
└── pyproject.toml       # Dependency management
```

---

**Contact:** [Your Name] - Data Engineering Portfolio
