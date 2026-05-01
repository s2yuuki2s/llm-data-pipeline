#!/bin/bash
# LLM Data Pipeline Orchestrator
# Automates Ingestion, EDA, and Spark ETL

set -e

# Visual formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=============================================================${NC}"
echo -e "${BLUE}          LLM DATA PIPELINE - AUTOMATED RUNNER               ${NC}"
echo -e "${BLUE}=============================================================${NC}"
echo ""

# Environment Validation
echo -e "${YELLOW}Validating environment...${NC}"
if ! command -v java &>/dev/null; then
  echo -e "${RED}Java not found. Please install OpenJDK 17+.${NC}"
  exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | cut -d'.' -f1)
if [ "$JAVA_VERSION" -lt 17 ]; then
  echo -e "${RED}Java version $JAVA_VERSION detected. Required: 17+.${NC}"
  exit 1
fi
echo -e "${GREEN}Java $JAVA_VERSION detected.${NC}"
echo ""

# Stage 1: Data Ingestion
echo -e "${BLUE}-------------------------------------------------------------${NC}"
echo -e "${YELLOW}Stage 1/3: Data Ingestion (Hugging Face)${NC}"
echo -e "${BLUE}-------------------------------------------------------------${NC}"

if [ -f "data/raw/dolly_15k.jsonl" ]; then
  echo -e "${YELLOW}Raw data already exists at data/raw/dolly_15k.jsonl${NC}"
  read -p "Force re-download? (y/N): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    uv run python -m src.ingest
  else
    echo -e "${GREEN}Skipping ingestion.${NC}"
  fi
else
  uv run python -m src.ingest
fi
echo ""

# Stage 2: Exploratory Data Analysis (Polars)
echo -e "${BLUE}-------------------------------------------------------------${NC}"
echo -e "${YELLOW}Stage 2/3: Profiling & EDA (Polars)${NC}"
echo -e "${BLUE}-------------------------------------------------------------${NC}"
uv run python -m src.explore
echo ""

# Stage 3: Spark ETL Transformation
echo -e "${BLUE}-------------------------------------------------------------${NC}"
echo -e "${YELLOW}Stage 3/3: Distributed ETL (PySpark)${NC}"
echo -e "${BLUE}-------------------------------------------------------------${NC}"
uv run python -m src.transform
echo ""

# Verification: Testing
echo -e "${BLUE}-------------------------------------------------------------${NC}"
echo -e "${YELLOW}Validation: Running Unit Tests${NC}"
echo -e "${BLUE}-------------------------------------------------------------${NC}"

read -p "Execute test suite? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
  uv run pytest -v
else
  echo -e "${YELLOW}Skipping tests.${NC}"
fi
echo ""

# Final Summary
echo -e "${GREEN}=============================================================${NC}"
echo -e "${GREEN}           PIPELINE EXECUTION SUCCESSFUL!                    ${NC}"
echo -e "${GREEN}=============================================================${NC}"
echo ""
echo -e "${BLUE}Assets Generated:${NC}"
echo -e "   - Raw Data:      data/raw/dolly_15k.jsonl"
echo -e "   - Processed:     data/processed/dolly_cleaned.parquet/ (Partitioned)"
echo -e "   - Audit Log:     data/processed/audit_log.json"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "   - Query data: ${BLUE}uv run python -c 'import polars as pl; print(pl.read_parquet(\"data/processed/dolly_cleaned.parquet\").head())'${NC}"
echo -e "   - Documentation: Check README.md for architecture details."
echo ""
