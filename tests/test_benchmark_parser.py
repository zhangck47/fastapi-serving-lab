from benchmark_parser import (
    SAMPLE_RECORDS,
    SAMPLE_RESULT,
    collect_model_names,
    filter_successful_records,
    summarize_record,
)


def test_summarize_record_builds_expected_metrics() -> None:
    summary = summarize_record(SAMPLE_RESULT)

    assert summary == {
        "request_id": "req_demo_001",
        "model": "mock-llm",
        "labels": ["mock", "cache-hit"],
        "total_tokens": 20,
        "tokens_per_second": 12.5,
    }


def test_filter_successful_records_keeps_only_success() -> None:
    result = filter_successful_records(SAMPLE_RECORDS)

    assert [record["request_id"] for record in result] == [
        "req_demo_001",
        "req_demo_003",
    ]


def test_collect_model_names_deduplicates_and_sorts() -> None:
    models = collect_model_names(SAMPLE_RECORDS)

    assert models == ("fast-llm", "mock-llm")


def test_collect_model_names_empty_records() -> None:
    assert collect_model_names([]) == ()


def test_successful_flow_uses_both_functions() -> None:
    models = collect_model_names(filter_successful_records(SAMPLE_RECORDS))

    assert models == ("fast-llm", "mock-llm")
