from benchmark_parser import SAMPLE_RESULT, summarize_record


def test_summarize_record_builds_expected_metrics() -> None:
    summary = summarize_record(SAMPLE_RESULT)

    assert summary == {
        "request_id": "req_demo_001",
        "model": "mock-llm",
        "labels": ["mock", "cache-hit"],
        "total_tokens": 20,
        "tokens_per_second": 12.5,
    }

