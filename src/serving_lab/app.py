"""FastAPI application for the serving lab."""

from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    """Return the current service health status."""

    return {"status": "ok"}
