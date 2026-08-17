"""File loaders for JSON and JSONL benchmark records."""

import json
from pathlib import Path


def load_benchmark_record(file_path: Path) -> dict[str, object]:
    """Read one benchmark record from a UTF-8 JSON file."""

    try:
        file_contents: str = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Benchmark file not found: {file_path}") from exc

    try:
        record: dict[str, object] = json.loads(file_contents)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in benchmark file: {file_path}") from exc

    return record


def load_benchmark_records(file_path: Path) -> list[dict[str, object]]:
    """Read benchmark records from a UTF-8 JSONL file."""

    records: list[dict[str, object]] = []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                record: dict[str, object] = json.loads(line)
                records.append(record)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Benchmark JSONL file not found: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON on line {line_number} in benchmark file: {file_path}"
        ) from exc

    return records

