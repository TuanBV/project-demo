from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_categories_empty(client: TestClient) -> None:
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert response.json() == []
