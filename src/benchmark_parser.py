"""Helpers for reading and processing sanitized benchmark records."""

import json
from pathlib import Path


SAMPLE_RESULT: dict[str, object] = {
    "request_id": "req_demo_001",
    "model": "mock-llm",
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "latency_ms": 640.0,
    "labels": ["mock", "cache-hit"],
}


def summarize_record(record: dict[str, object]) -> dict[str, object]:
    """Build a small summary from one already-decoded benchmark record."""

    # Day 1: 从字典取值，并保存到带类型标注的变量中。
    request_id: str = record["request_id"]
    model: str = record["model"]
    labels: list[str] = record["labels"]
    prompt_tokens: int = record["prompt_tokens"]
    completion_tokens: int = record["completion_tokens"]
    latency_ms: float = record["latency_ms"]

    # Day 1: 计算 total_tokens 和 tokens_per_second。
    # tokens_per_second = completion_tokens / (latency_ms / 1000)
    total_tokens: int = prompt_tokens + completion_tokens
    tokens_per_second: float = completion_tokens / (latency_ms / 1000)

    # Day 1: 返回一个新的汇总字典。
    return {
        "request_id": request_id,
        "model": model,
        "labels": labels,
        "total_tokens": total_tokens,
        "tokens_per_second": tokens_per_second
    }


SAMPLE_RECORDS: list[dict[str, object]] = [
    {
        "request_id": "req_demo_001",
        "model": "mock-llm",
        "status": "success",
        "prompt_tokens": 12,
        "completion_tokens": 8,
        "latency_ms": 640.0,
        "labels": ["mock", "cache-hit"],
    },
    {
        "request_id": "req_demo_002",
        "model": "mock-llm",
        "status": "failed",
        "prompt_tokens": 6,
        "completion_tokens": 0,
        "latency_ms": 500.0,
        "labels": ["mock", "timeout"],
    },
    {
        "request_id": "req_demo_003",
        "model": "fast-llm",
        "status": "success",
        "prompt_tokens": 10,
        "completion_tokens": 5,
        "latency_ms": 300.0,
        "labels": ["mock", "cache-hit"],
    },
]


def filter_successful_records(
    records: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Filter records whose status is "success", keeping original order."""

    # Day 2: 遍历记录，保留 status 为 success 的项目。
    successful: list[dict[str, object]] = []
    for record in records:
        if record["status"] == "success":
            successful.append(record)
    return successful


def collect_model_names(records: list[dict[str, object]]) -> tuple[str, ...]:
    """Return unique model names as a sorted tuple."""

    # Day 2: 使用集合对模型名去重。
    models: set[str] = set()
    for record in records:
        models.add(record["model"])
    return tuple(sorted(models))


def load_benchmark_record(file_path: Path) -> dict[str, object]:
    """Read one benchmark record from a UTF-8 JSON file."""

    try:
        # TODO 1: 使用 file_path.read_text(encoding="utf-8") 读取文件，
        # 将结果保存到带 str 类型标注的 file_contents 变量。
        file_contents: str = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        # TODO 2: 抛出新的 FileNotFoundError，消息包含：
        # Benchmark file not found: <文件路径>
        # 使用 "raise ... from exc" 保留原始异常原因。
        raise FileNotFoundError(f"Benchmark file not found: {file_path}") from exc

    try:
        # TODO 3: 使用 json.loads(file_contents) 解码 JSON，保存到 record，
        # 然后返回 record。若发生 json.JSONDecodeError，则在 except 中
        # 抛出 ValueError，消息包含：Invalid JSON in benchmark file: <文件路径>，
        # 同样使用 "raise ... from exc"。
        record: dict[str, object] = json.loads(file_contents)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in benchmark file: {file_path}") from exc

    return record
