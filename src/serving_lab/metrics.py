"""Calculations and filtering for benchmark records."""


SAMPLE_RESULT: dict[str, object] = {
    "request_id": "req_demo_001",
    "model": "mock-llm",
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "latency_ms": 640.0,
    "labels": ["mock", "cache-hit"],
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


def summarize_record(record: dict[str, object]) -> dict[str, object]:
    """Build a small summary from one already-decoded benchmark record."""

    request_id: str = record["request_id"]
    model: str = record["model"]
    labels: list[str] = record["labels"]
    prompt_tokens: int = record["prompt_tokens"]
    completion_tokens: int = record["completion_tokens"]
    latency_ms: float = record["latency_ms"]

    total_tokens: int = prompt_tokens + completion_tokens
    tokens_per_second: float = completion_tokens / (latency_ms / 1000)

    return {
        "request_id": request_id,
        "model": model,
        "labels": labels,
        "total_tokens": total_tokens,
        "tokens_per_second": tokens_per_second,
    }


def filter_successful_records(
    records: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Filter records whose status is "success", keeping original order."""

    successful: list[dict[str, object]] = []
    for record in records:
        if record["status"] == "success":
            successful.append(record)
    return successful


def collect_model_names(records: list[dict[str, object]]) -> tuple[str, ...]:
    """Return unique model names as a sorted tuple."""

    models: set[str] = set()
    for record in records:
        models.add(record["model"])
    return tuple(sorted(models))

