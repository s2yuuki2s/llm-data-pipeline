import pytest
import pyspark.sql.functions as F
from src.transform import (
    create_spark_session,
    get_dolly_schema,
    clean_data,
    enrich_data,
    filter_data,
    compute_audit_log,
)


@pytest.fixture(scope="module")
def spark():
    spark = create_spark_session("UnitTests")
    yield spark
    spark.stop()


@pytest.fixture
def sample_df(spark):
    data = [
        ("What is Python?", "Context here", "Python is a language", "general_qa"),
        ("  Dirty Text  ", None, "  This is a valid response length.  ", "general_qa"),
        (
            "What is Python?",
            "Context here",
            "Python is a language",
            "general_qa",
        ),  # Duplicate
        ("Short", "", "Too short", "test"),  # Invalid
    ]
    return spark.createDataFrame(data, schema=get_dolly_schema())


def test_clean_data(sample_df):
    cleaned = clean_data(sample_df)

    # 1 duplicate removed -> 3 rows
    assert cleaned.count() == 3

    # Check trimming
    dirty_row = cleaned.filter(F.col("instruction") == "Dirty Text").collect()[0]
    assert dirty_row["instruction"] == "Dirty Text"
    assert dirty_row["response"] == "This is a valid response length."

    # Check null context handling
    assert dirty_row["context"] == ""


def test_enrich_data(spark, sample_df):
    cleaned = clean_data(sample_df)
    enriched = enrich_data(cleaned)

    assert "instruction_length" in enriched.columns
    assert "combined_text" in enriched.columns

    row = enriched.filter(F.col("instruction") == "What is Python?").collect()[0]
    assert row["instruction_length"] == len("What is Python?")
    assert "Instruction:" in row["combined_text"]


def test_filter_data(spark, sample_df):
    cleaned = clean_data(sample_df)
    enriched = enrich_data(cleaned)
    filtered = filter_data(enriched)

    # Only "What is Python?" and "Dirty Text" should survive
    # "Short" record is too short for instruction/response
    assert filtered.count() == 2


def test_audit_summary(spark, sample_df):
    cleaned = clean_data(sample_df)
    enriched = enrich_data(cleaned)
    filtered = filter_data(enriched)

    summary = compute_audit_log(spark, filtered)

    assert summary["total_records"] == 2
    assert summary["unique_categories"] == 1
    assert "timestamp" in summary
