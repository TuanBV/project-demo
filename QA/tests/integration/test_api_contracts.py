"""Spec section 22 'API' checklist items not already covered by the three main flows."""

from __future__ import annotations

import io

import pytest
from fastapi.testclient import TestClient


def _create_category_and_question(client: TestClient, name: str = "Contract Test") -> dict:
    category = client.post("/api/admin/categories", json={"name": name}).json()
    question = client.post(
        "/api/admin/questions",
        json={
            "category_id": category["id"],
            "content": f"Cau hoi {name}?",
            "options": [
                {"content": "Dap an dung.", "is_correct": True},
                {"content": "Dap an sai 1.", "is_correct": False},
                {"content": "Dap an sai 2.", "is_correct": False},
                {"content": "Dap an sai 3.", "is_correct": False},
            ],
        },
    ).json()
    return {"category": category, "question": question}


def test_study_api_does_not_leak_keywords_or_concepts(client: TestClient) -> None:
    ctx = _create_category_and_question(client)
    study_question = client.get(f"/api/questions/{ctx['question']['id']}").json()
    assert "concepts" not in study_question
    assert "contradiction_rules" not in study_question
    assert "java_answer" not in study_question
    assert "is_correct" not in study_question["options"][0]


def test_evaluate_updates_question_progress(client: TestClient) -> None:
    ctx = _create_category_and_question(client)
    question_id = ctx["question"]["id"]
    correct_option_id = next(o["id"] for o in ctx["question"]["options"] if o["is_correct"])
    session = client.post("/api/study-sessions", json={"mode": "RANDOM"}).json()
    client.post(f"/api/study-sessions/{session['id']}/next")
    client.post(
        f"/api/study-sessions/{session['id']}/questions/{question_id}/answer",
        json={"selected_option_id": correct_option_id},
    )
    weak = client.get("/api/progress/weak-questions").json()
    overview = client.get("/api/progress/overview").json()
    assert overview["attempted_questions"] == 1
    assert overview["correct_count"] == 1
    assert isinstance(weak, list)


def test_random_exclude_ids_works(client: TestClient) -> None:
    ctx = _create_category_and_question(client, name="Exclude Test")
    question_id = ctx["question"]["id"]
    response = client.get(f"/api/questions/random?exclude_ids={question_id}")
    assert response.status_code == 404


def test_filter_by_category_works(client: TestClient) -> None:
    ctx1 = _create_category_and_question(client, name="Cat A")
    _create_category_and_question(client, name="Cat B")
    response = client.get(f"/api/questions?category_id={ctx1['category']['id']}")
    body = response.json()
    assert len(body) == 1
    assert body[0]["category"]["name"] == "Cat A"


def test_docx_upload_too_large_is_rejected(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.core.config import Settings

    tiny_settings = Settings(max_docx_upload_size_mb=0)
    monkeypatch.setattr("app.api.routes.imports.get_settings", lambda: tiny_settings)

    files = {
        "file": (
            "big.docx",
            io.BytesIO(b"x" * 2048),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    response = client.post("/api/admin/import/docx", files=files, data={"dry_run": "true"})
    assert response.status_code == 413


def test_empty_pasted_text_is_rejected(client: TestClient) -> None:
    response = client.post("/api/admin/import/text", json={"content": "   ", "dry_run": True})
    assert response.status_code == 422
