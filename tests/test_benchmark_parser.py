from pathlib import Path

import pytest
import serving_lab

from serving_lab.loaders import load_benchmark_record, load_benchmark_records
from serving_lab.metrics import (
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


def test_load_benchmark_record_reads_json(tmp_path: Path) -> None:
    benchmark_file = tmp_path / "benchmark.json"
    benchmark_file.write_text(
        '{"request_id": "req_file_001", "model": "mock-llm"}',
        encoding="utf-8",
    )

    record = load_benchmark_record(benchmark_file)

    assert record == {
        "request_id": "req_file_001",
        "model": "mock-llm",
    }


def test_load_benchmark_record_reports_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError, match="Benchmark file not found"):
        load_benchmark_record(missing_file)


def test_load_benchmark_record_reports_invalid_json(tmp_path: Path) -> None:
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text('{"request_id": }', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON in benchmark file"):
        load_benchmark_record(invalid_file)


def test_load_benchmark_records_reads_jsonl_and_skips_blank_lines(
    tmp_path: Path,
) -> None:
    jsonl_file = tmp_path / "benchmark.jsonl"
    jsonl_file.write_text(
        '{"request_id": "req_001", "model": "mock-llm"}\n'
        "\n"
        '{"request_id": "req_002", "model": "fast-llm"}\n',
        encoding="utf-8",
    )

    records = load_benchmark_records(jsonl_file)

    assert records == [
        {"request_id": "req_001", "model": "mock-llm"},
        {"request_id": "req_002", "model": "fast-llm"},
    ]


def test_load_benchmark_records_returns_empty_list_for_empty_file(
    tmp_path: Path,
) -> None:
    empty_file = tmp_path / "empty.jsonl"
    empty_file.write_text("", encoding="utf-8")

    assert load_benchmark_records(empty_file) == []


def test_load_benchmark_records_reports_bad_line_number(tmp_path: Path) -> None:
    invalid_file = tmp_path / "invalid.jsonl"
    invalid_file.write_text(
        '{"request_id": "req_001"}\n'
        '{"request_id": }\n'
        '{"request_id": "req_003"}\n',
        encoding="utf-8",
    )

    expected_message = "Invalid JSON on line 2 in benchmark file"
    with pytest.raises(ValueError, match=expected_message):
        load_benchmark_records(invalid_file)


def test_package_exposes_metric_helpers() -> None:
    assert serving_lab.summarize_record is summarize_record
    assert serving_lab.filter_successful_records is filter_successful_records
    assert serving_lab.collect_model_names is collect_model_names


def test_package_exposes_loader_helpers() -> None:
    assert serving_lab.load_benchmark_record is load_benchmark_record
    assert serving_lab.load_benchmark_records is load_benchmark_records


def test_package_declares_public_api() -> None:
    assert serving_lab.__all__ == [
        "SAMPLE_RECORDS",
        "SAMPLE_RESULT",
        "collect_model_names",
        "filter_successful_records",
        "summarize_record",
        "load_benchmark_record",
        "load_benchmark_records",
    ]
