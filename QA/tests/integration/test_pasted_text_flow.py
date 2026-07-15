"""Spec section 23 'Luồng pasted text' (multiple-choice): paste question+answer-only text
-> preview -> import as NEEDS_REVIEW draft (auto-generated distractors) -> admin reviews
and supplies real options -> validate -> study.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

TEXT_CONTENT = """CATEGORY: Python Core
TYPE: TEXT
QUESTION: Generator la gi?
ANSWER: Generator la iterator sinh du lieu lazy bang yield.
KEYWORDS: generator, iterator, lazy, yield
---

CATEGORY: Python Core
TYPE: TEXT
QUESTION: List comprehension la gi?
ANSWER: List comprehension la cu phap ngan gon de tao list moi tu mot iterable.
KEYWORDS: list comprehension, iterable
"""


def test_pasted_text_dry_run_preview(client: TestClient) -> None:
    response = client.post(
        "/api/admin/import/text", json={"content": TEXT_CONTENT, "dry_run": True}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["questions_detected"] == 2
    assert body["summary"]["questions_created"] == 0


def test_pasted_text_import_needs_review_then_edit_then_validate_then_study(
    client: TestClient,
) -> None:
    imported = client.post(
        "/api/admin/import/text", json={"content": TEXT_CONTENT, "dry_run": False}
    ).json()
    assert imported["summary"]["questions_created"] == 2
    assert imported["summary"]["questions_needs_review"] == 2
    assert all(item["status"] == "NEEDS_REVIEW" for item in imported["items"])

    admin_questions = client.get("/api/admin/questions").json()
    assert len(admin_questions) == 2
    question_id = admin_questions[0]["id"]

    detail = client.get(f"/api/admin/questions/{question_id}").json()
    assert detail["needs_review"] is True
    assert detail["active"] is False
    assert len(detail["options"]) == 4
    assert sum(1 for o in detail["options"] if o["is_correct"]) == 1

    # Admin reviews and supplies proper hand-written options, then activates the question.
    update_response = client.put(
        f"/api/admin/questions/{question_id}",
        json={
            "active": True,
            "needs_review": False,
            "options": [
                {
                    "content": "Generator la iterator sinh du lieu lazy bang yield.",
                    "is_correct": True,
                },
                {"content": "Mot loai vong lap chi dung cho danh sach.", "is_correct": False},
                {"content": "Mot ham quan ly bo nho tu dong.", "is_correct": False},
                {"content": "Mot thu vien xu ly file trong Python.", "is_correct": False},
            ],
        },
    )
    assert update_response.status_code == 200
    updated_detail = update_response.json()
    assert updated_detail["active"] is True
    assert updated_detail["needs_review"] is False

    validation = client.post(f"/api/admin/questions/{question_id}/validate").json()
    assert validation["status"] == "VALID"

    session = client.post("/api/study-sessions", json={"mode": "RANDOM"}).json()
    question = client.post(f"/api/study-sessions/{session['id']}/next").json()
    assert question["id"] == question_id
    assert "options" in question
    correct_option_id = next(o["id"] for o in updated_detail["options"] if o["is_correct"])

    answer = client.post(
        f"/api/study-sessions/{session['id']}/questions/{question_id}/answer",
        json={"selected_option_id": correct_option_id},
    )
    assert answer.status_code == 200
