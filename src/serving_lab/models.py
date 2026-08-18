"""Typed data objects for benchmark records and summaries."""

from dataclasses import dataclass


@dataclass
class BenchmarkRecord:
    """One parsed benchmark request."""

    request_id: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    labels: list[str]
    status: str
    cache_hit: bool | None = None


@dataclass
class BenchmarkSummary:
    """Calculated metrics for one benchmark request."""

    request_id: str
    model: str
    total_tokens: int
    tokens_per_second: float
    cache_hit: bool | None


def benchmark_record_from_dict(data: dict[str, object]) -> BenchmarkRecord:
    """Convert one decoded JSON dictionary into a BenchmarkRecord."""

    return BenchmarkRecord(
        request_id=data["request_id"],
        model=data["model"],
        prompt_tokens=data["prompt_tokens"],
        completion_tokens=data["completion_tokens"],
        latency_ms=data["latency_ms"],
        labels=data["labels"],
        status=data["status"],
        cache_hit=data.get("cache_hit"),
    )


def summarize_benchmark_record(record: BenchmarkRecord) -> BenchmarkSummary:
    """Calculate a typed summary from one benchmark record."""

    total_tokens: int = record.prompt_tokens + record.completion_tokens
    tokens_per_second: float = record.completion_tokens / (
        record.latency_ms / 1000
    )

    return BenchmarkSummary(
        request_id=record.request_id,
        model=record.model,
        total_tokens=total_tokens,
        tokens_per_second=tokens_per_second,
        cache_hit=record.cache_hit,
    )
