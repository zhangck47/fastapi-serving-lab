"""End-to-end benchmark parsing and summary pipeline."""

from collections.abc import Iterator
from pathlib import Path

from .loaders import iter_benchmark_records
from .models import (
    BenchmarkSummary,
    benchmark_record_from_dict,
    summarize_benchmark_record,
)


def iter_benchmark_summaries(
    file_path: Path,
) -> Iterator[BenchmarkSummary]:
    """Yield typed summaries from a JSONL benchmark file."""

    for record_dict in iter_benchmark_records(file_path):
        benchmark_record = benchmark_record_from_dict(record_dict)
        summary = summarize_benchmark_record(benchmark_record)
        yield summary
