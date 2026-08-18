from dataclasses import is_dataclass

from serving_lab.models import (
    BenchmarkRecord,
    BenchmarkSummary,
    benchmark_record_from_dict,
    summarize_benchmark_record,
)


SAMPLE_RECORD_DATA: dict[str, object] = {
    "request_id": "req_model_001",
    "model": "mock-llm",
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "latency_ms": 640.0,
    "labels": ["mock", "cache-hit"],
    "status": "success",
    "cache_hit": True,
}


def test_benchmark_record_is_dataclass_with_optional_default() -> None:
    record = BenchmarkRecord(
        request_id="req_model_001",
        model="mock-llm",
        prompt_tokens=12,
        completion_tokens=8,
        latency_ms=640.0,
        labels=["mock"],
        status="success",
    )

    assert is_dataclass(record)
    assert record.cache_hit is None


def test_benchmark_record_from_dict_preserves_cache_hit() -> None:
    record = benchmark_record_from_dict(SAMPLE_RECORD_DATA)

    assert record == BenchmarkRecord(
        request_id="req_model_001",
        model="mock-llm",
        prompt_tokens=12,
        completion_tokens=8,
        latency_ms=640.0,
        labels=["mock", "cache-hit"],
        status="success",
        cache_hit=True,
    )


def test_benchmark_record_from_dict_defaults_missing_cache_hit() -> None:
    data_without_cache_hit = SAMPLE_RECORD_DATA.copy()
    data_without_cache_hit.pop("cache_hit")

    record = benchmark_record_from_dict(data_without_cache_hit)

    assert record.cache_hit is None


def test_summarize_benchmark_record_returns_typed_summary() -> None:
    record = benchmark_record_from_dict(SAMPLE_RECORD_DATA)

    summary = summarize_benchmark_record(record)

    assert summary == BenchmarkSummary(
        request_id="req_model_001",
        model="mock-llm",
        total_tokens=20,
        tokens_per_second=12.5,
        cache_hit=True,
    )
