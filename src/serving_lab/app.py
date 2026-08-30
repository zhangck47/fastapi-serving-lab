"""FastAPI application for the serving lab."""

from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    """Return the current service health status."""

    return {"status": "ok"}


@app.get("/debug/models/{model_name}")
def inspect_model_parameters(
    model_name: str,
    limit: int = 1,
) -> dict[str, object]:
    """Return path and query values so their sources are visible."""

    return {"model": model_name, "limit": limit}
