from collections.abc import Iterator
from pathlib import Path

import pytest

from serving_lab.loaders import iter_benchmark_records


def test_iter_benchmark_records_defers_opening_until_next(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.jsonl"

    records = iter_benchmark_records(missing_file)

    assert isinstance(records, Iterator)
    with pytest.raises(FileNotFoundError, match="Benchmark JSONL file not found"):
        next(records)


def test_iter_benchmark_records_yields_in_order_and_skips_blanks(
    tmp_path: Path,
) -> None:
    jsonl_file = tmp_path / "benchmark.jsonl"
    jsonl_file.write_text(
        '{"request_id": "req_001"}\n'
        "\n"
        '{"request_id": "req_002"}\n',
        encoding="utf-8",
    )

    records = list(iter_benchmark_records(jsonl_file))

    assert records == [
        {"request_id": "req_001"},
        {"request_id": "req_002"},
    ]


def test_iter_benchmark_records_can_stop_before_later_bad_line(
    tmp_path: Path,
) -> None:
    jsonl_file = tmp_path / "benchmark.jsonl"
    jsonl_file.write_text(
        '{"request_id": "req_001"}\n'
        '{"request_id": }\n',
        encoding="utf-8",
    )

    records = iter_benchmark_records(jsonl_file)

    assert next(records) == {"request_id": "req_001"}
    records.close()


def test_iter_benchmark_records_reports_bad_line_when_consumed(
    tmp_path: Path,
) -> None:
    jsonl_file = tmp_path / "benchmark.jsonl"
    jsonl_file.write_text(
        '{"request_id": "req_001"}\n'
        "\n"
        '{"request_id": }\n',
        encoding="utf-8",
    )
    records = iter_benchmark_records(jsonl_file)

    assert next(records) == {"request_id": "req_001"}
    with pytest.raises(ValueError, match="Invalid JSON on line 3"):
        next(records)
