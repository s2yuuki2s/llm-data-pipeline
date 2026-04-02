import json
import pytest
from src.transform import (
    create_spark_session,
    load_raw_data,
    clean_data,
    enrich_data,
    filter_data,
    compute_audit_log,
)


@pytest.fixture(scope="module")
def spark():
    spark = create_spark_session("IntegrationTest")
    yield spark
    spark.stop()


def test_full_pipeline_integration(spark, tmp_path):
    """
    End-to-End Integration Test:
    1. Create a dummy raw JSONL file.
    2. Load, Clean, Enrich, Filter.
    3. Verify final schema and data quality metrics.
    """
    # 1. Setup mock raw data
    raw_file = tmp_path / "mock_dolly.jsonl"
    mock_data = [
        {
            "instruction": "What is Spark?",
            "context": "",
            "response": "Apache Spark is a unified engine for data processing.",
            "category": "general_qa",
        },
        {
            "instruction": "Bad",
            "context": "",
            "response": "Short",
            "category": "noise",
        },  # Should be filtered
        {
            "instruction": "  Trim me  ",
            "context": None,
            "response": "This is a valid response length string for testing.",
            "category": "creative_writing",
        },
    ]

    with open(raw_file, "w") as f:
        for item in mock_data:
            f.write(json.dumps(item) + "\n")

    # 2. Execution
    df_raw = load_raw_data(spark, raw_file)
    df_clean = clean_data(df_raw)
    df_enriched = enrich_data(df_clean)
    df_final = filter_data(df_enriched)

    # 3. Validation
    # - "Bad" record should be filtered out (2 remain)
    # - "Trim me" should be cleaned
    # - Metadata should be present
    final_count = df_final.count()
    assert final_count == 2

    # Check Spark SQL Audit
    audit = compute_audit_log(spark, df_final)
    assert audit["total_records"] == 2
    assert audit["unique_categories"] == 2
    assert audit["avg_instruction_len"] > 0

    # Check specific cleansing
    trimmed_row = df_final.filter(df_final.instruction == "Trim me").collect()[
        0
    ]
    assert trimmed_row["instruction"] == "Trim me"
    assert trimmed_row["context"] == ""
    assert "Instruction:" in trimmed_row["combined_text"]
