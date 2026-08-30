"""HTTP tests for path and query parameters."""

from fastapi.testclient import TestClient

from serving_lab.app import app


client = TestClient(app)


def test_parameter_route_reads_path_and_query_values() -> None:
    response = client.get("/debug/models/mock-llm?limit=3")

    assert response.status_code == 200
    assert response.json() == {"model": "mock-llm", "limit": 3}


def test_parameter_route_uses_default_query_value() -> None:
    response = client.get("/debug/models/fast-llm")

    assert response.status_code == 200
    assert response.json() == {"model": "fast-llm", "limit": 1}


def test_parameter_route_rejects_invalid_query_type() -> None:
    response = client.get("/debug/models/mock-llm?limit=many")

    assert response.status_code == 422
