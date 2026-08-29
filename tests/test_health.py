"""HTTP-level tests for the health endpoint."""

from fastapi.testclient import TestClient

from serving_lab.app import app


client = TestClient(app)


def test_health_returns_success_status_code() -> None:
    response = client.get("/health")

    assert response.status_code == 200


def test_health_returns_expected_json_body() -> None:
    response = client.get("/health")

    assert response.json() == {"status": "ok"}


def test_health_rejects_post_method() -> None:
    response = client.post("/health")

    assert response.status_code == 405
