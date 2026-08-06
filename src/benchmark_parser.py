"""Day 1: summarize one sanitized benchmark result."""


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
    request_id: str = ""
    model: str = ""
    labels: list[str] = []
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0

    # TODO 2: 计算 total_tokens 和 tokens_per_second。
    # tokens_per_second = completion_tokens / (latency_ms / 1000)
    total_tokens: int = 0
    tokens_per_second: float = 0.0

    # TODO 3: 返回包含五个目标字段的新 dict；字段名以 README 的期望汇总为准。
    return {}

