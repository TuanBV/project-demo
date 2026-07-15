"""Confirms the legacy FREE_TEXT attempt/evaluate endpoints still work after the
multiple-choice migration (spec: don't break code kept for FREE_TEXT questions)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_legacy_free_text_attempt_endpoint_still_works(client: TestClient) -> None:
    category = client.post("/api/admin/categories", json={"name": "Legacy FT Cat"}).json()
    question = client.post(
        "/api/admin/questions",
        json={
            "category_id": category["id"],
            "question_format": "FREE_TEXT",
            "content": "JVM la gi?",
            "reference_answer": "JVM la may ao thuc thi Java bytecode.",
            "concepts": [
                {
                    "name": "main",
                    "description": "JVM thuc thi bytecode",
                    "weight": 100,
                    "required": True,
                    "keywords": [{"keyword": "bytecode", "match_type": "CONTAINS"}],
                }
            ],
        },
    ).json()
    assert question["question_format"] == "FREE_TEXT"

    session = client.post("/api/study-sessions", json={"mode": "RANDOM"}).json()
    response = client.post(
        f"/api/study-sessions/{session['id']}/attempts",
        json={"question_id": question["id"], "submitted_answer": "JVM thuc thi Java bytecode"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 100.0
    assert body["classification"] == "CORRECT"

    evaluate_response = client.post(
        f"/api/questions/{question['id']}/evaluate",
        json={"question_id": question["id"], "submitted_answer": "JVM thuc thi Java bytecode"},
    )
    assert evaluate_response.status_code == 200
    assert evaluate_response.json()["score"] == 100.0
