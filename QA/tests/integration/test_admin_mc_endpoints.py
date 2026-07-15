"""Integration coverage for the MC-specific admin endpoints (spec section 13)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_mc_question(client: TestClient, category_name: str = "Admin MC Cat") -> dict:
    category = client.post("/api/admin/categories", json={"name": category_name}).json()
    return client.post(
        "/api/admin/questions",
        json={
            "category_id": category["id"],
            "content": "JVM la gi?",
            "options": [
                {"content": "May ao thuc thi Java bytecode.", "is_correct": True},
                {"content": "Trinh bien dich.", "is_correct": False},
                {"content": "Thu vien giao dien.", "is_correct": False},
                {"content": "He quan tri CSDL.", "is_correct": False},
            ],
        },
    ).json()


def test_duplicate_endpoint(client: TestClient) -> None:
    question = _create_mc_question(client)
    response = client.post(f"/api/admin/questions/{question['id']}/duplicate")
    assert response.status_code == 201
    clone = response.json()
    assert clone["id"] != question["id"]
    assert clone["active"] is False


def test_generate_distractors_endpoint(client: TestClient) -> None:
    response = client.post(
        "/api/admin/questions/generate-distractors",
        json={
            "question": "Compiler la gi?",
            "correct_answer": "Compiler dich toan bo ma nguon truoc khi chay.",
            "count": 3,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["distractors"]) == 3


def test_regenerate_distractors_endpoint(client: TestClient) -> None:
    question = _create_mc_question(client, category_name="Regen Endpoint Cat")
    response = client.post(f"/api/admin/questions/{question['id']}/regenerate-distractors")
    assert response.status_code == 200
    body = response.json()
    assert len(body["options"]) == 4
    assert sum(1 for o in body["options"] if o["is_correct"]) == 1


def test_validate_endpoint(client: TestClient) -> None:
    question = _create_mc_question(client, category_name="Validate Endpoint Cat")
    response = client.post(f"/api/admin/questions/{question['id']}/validate")
    assert response.status_code == 200
    assert response.json()["status"] == "VALID"
