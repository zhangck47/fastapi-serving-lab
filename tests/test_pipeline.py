import json
from pathlib import Path

import pytest

from serving_lab.models import BenchmarkSummary
from serving_lab.pipeline import iter_benchmark_summaries


@pytest.mark.parametrize(
    ("record_data", "expected_total_tokens", "expected_tokens_per_second"),
    [
        (
            {
                "request_id": "req_normal",
                "model": "mock-llm",
                "prompt_tokens": 12,
                "completion_tokens": 8,
                "latency_ms": 640.0,
                "labels": [],
                "status": "success",
            },
            20,
            12.5,
        ),
        (
            {
                "request_id": "req_zero_completion",
                "model": "mock-llm",
                "prompt_tokens": 6,
                "completion_tokens": 0,
                "latency_ms": 500.0,
                "labels": [],
                "status": "success",
            },
            6,
            0.0,
        ),
        (
            {
                "request_id": "req_zero_prompt",
                "model": "mock-llm",
                "prompt_tokens": 0,
                "completion_tokens": 5,
                "latency_ms": 250.0,
                "labels": [],
                "status": "success",
            },
            5,
            20.0,
        ),
    ],
)
def test_iter_benchmark_summaries_calculates_parameterized_metrics(
    tmp_path: Path,
    record_data: dict[str, object],
    expected_total_tokens: int,
    expected_tokens_per_second: float,
) -> None:
    jsonl_file = tmp_path / "benchmark.jsonl"
    jsonl_file.write_text(json.dumps(record_data) + "\n", encoding="utf-8")

    summaries = list(iter_benchmark_summaries(jsonl_file))

    assert len(summaries) == 1
    summary = summaries[0]
    assert isinstance(summary, BenchmarkSummary)
    assert summary.total_tokens == expected_total_tokens
    assert summary.tokens_per_second == expected_tokens_per_second


def test_iter_benchmark_summaries_preserves_lazy_bad_line_error(
    tmp_path: Path,
) -> None:
    jsonl_file = tmp_path / "benchmark.jsonl"
    jsonl_file.write_text(
        '{"request_id":"req_first","model":"mock-llm",'
        '"prompt_tokens":1,"completion_tokens":1,"latency_ms":100.0,'
        '"labels":[],"status":"success"}\n'
        '{"request_id":}\n',
        encoding="utf-8",
    )

    summaries = iter_benchmark_summaries(jsonl_file)

    assert next(summaries).request_id == "req_first"
    with pytest.raises(ValueError, match="Invalid JSON on line 2"):
        next(summaries)
