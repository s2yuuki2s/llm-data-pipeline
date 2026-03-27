# LLM Data Pipeline

This project is a simple ETL pipeline to process data from Hugging Face (Dolly-15k dataset) for LLM data preparation.

## Directory Structure
- `data/`: Contains raw data and processed data.
- `src/`: Main source code of the project.
  - `config.py`: Manages paths and configuration parameters.
  - `ingest.py`: Downloads data from Hugging Face and saves it locally.
  - `explore.py`: Fast data analysis (EDA) using Polars.
- `tests/`: Basic test scripts.
- `pyproject.toml`: Library declarations and `uv` configuration.

## Installation
Requires `uv` to be installed on your system.

```bash
uv sync
```

## How to Run

### 1. Data Ingestion
This command will download the `databricks-dolly-15k` dataset to the `data/raw/` directory.

```bash
uv run python -m src.ingest
```

### 2. Data Exploration
Use Polars to check the data structure and basic statistics.

```bash
uv run python -m src.explore
```

### 3. Code Quality Check
Run the linter and unit tests to ensure no syntax or basic logic errors.

```bash
uv run ruff check .
uv run pytest
```
