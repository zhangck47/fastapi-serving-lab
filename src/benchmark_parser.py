"""Benchmark record helpers: summary (Day 1) and success filtering (Day 2)."""


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

    # TODO 1: 从 record 取出 request_id、model、labels 和三个数值字段，
    # 并分别保存到带类型标注的变量中。
    request_id: str = record["request_id"]
    model: str = record["model"]
    labels: list[str] = record["labels"]
    prompt_tokens: int = record["prompt_tokens"]
    completion_tokens: int = record["completion_tokens"]
    latency_ms: float = record["latency_ms"]

    # TODO 2: 计算 total_tokens 和 tokens_per_second。
    # tokens_per_second = completion_tokens / (latency_ms / 1000)
    total_tokens: int = prompt_tokens + completion_tokens
    tokens_per_second: float = completion_tokens / (latency_ms / 1000)

    # TODO 3: 返回包含五个目标字段的新 dict；字段名以 README 的期望汇总为准。
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

    # TODO 1: 用 for 循环遍历 records，用 if 判断 record["status"] == "success"，
    # 把满足条件的记录 append 到 successful。
    successful: list[dict[str, object]] = []
    for record in records:
        if record.get("status") == "success":
            successful.append(record)
    # TODO 2: 返回 successful。
    return successful


def collect_model_names(records: list[dict[str, object]]) -> tuple[str, ...]:
    """Return unique model names as a sorted tuple."""

    # TODO 3: 用 for 循环把所有 record["model"] 加入集合 models 去重。
    models: set[str] = set()
    for record in records:
        models.add(record.get("model"))
    # TODO 4: 用 sorted() 排序后转为 tuple 返回。
    return (tuple(sorted(models)))
