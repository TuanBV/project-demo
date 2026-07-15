"""Spec section 23 'Luồng manual' (multiple-choice): create category -> create MC question
with 4 options -> fetch study question (answer hidden, options shuffled) -> submit answer
-> check score -> check history -> check progress.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_manual_creation_and_study_flow(client: TestClient) -> None:
    category = client.post("/api/admin/categories", json={"name": "Manual Test Category"}).json()

    question = client.post(
        "/api/admin/questions",
        json={
            "category_id": category["id"],
            "content": "Immutable trong Python la gi?",
            "explanation": "Immutable la kieu du lieu khong the thay doi sau khi tao.",
            "options": [
                {"content": "Kieu du lieu khong the thay doi sau khi tao.", "is_correct": True},
                {"content": "Kieu du lieu co the thay doi bat ky luc nao.", "is_correct": False},
                {"content": "Mot loai vong lap dac biet trong Python.", "is_correct": False},
                {"content": "Mot thu vien quan ly bo nho cua Python.", "is_correct": False},
            ],
        },
    ).json()
    assert question["question_format"] == "MULTIPLE_CHOICE"
    assert len(question["options"]) == 4
    correct_option = next(o for o in question["options"] if o["is_correct"])

    study_question = client.get(f"/api/questions/{question['id']}").json()
    assert "is_correct" not in study_question["options"][0]
    assert "reference_answer" not in study_question
    assert "concepts" not in study_question
    assert len(study_question["options"]) == 4

    session = client.post("/api/study-sessions", json={"mode": "RANDOM"}).json()
    delivered = client.post(f"/api/study-sessions/{session['id']}/next").json()
    assert delivered["id"] == question["id"]
    delivered_option_ids = {o["id"] for o in delivered["options"]}
    assert delivered_option_ids == {o["id"] for o in question["options"]}

    answer = client.post(
        f"/api/study-sessions/{session['id']}/questions/{question['id']}/answer",
        json={"selected_option_id": correct_option["id"]},
    ).json()
    assert answer["is_correct"] is True
    assert answer["score"] == 100.0
    assert answer["correct_option_id"] == correct_option["id"]

    history = client.get("/api/history").json()
    assert len(history) == 1
    assert history[0]["question_id"] == question["id"]
    assert history[0]["is_correct"] is True

    overview = client.get("/api/progress/overview").json()
    assert overview["attempted_questions"] == 1
    assert overview["correct_count"] == 1


def test_double_submit_is_rejected(client: TestClient) -> None:
    category = client.post("/api/admin/categories", json={"name": "Double Submit Cat"}).json()
    question = client.post(
        "/api/admin/questions",
        json={
            "category_id": category["id"],
            "content": "Q?",
            "options": [
                {"content": "Dung.", "is_correct": True},
                {"content": "Sai 1.", "is_correct": False},
                {"content": "Sai 2.", "is_correct": False},
                {"content": "Sai 3.", "is_correct": False},
            ],
        },
    ).json()
    correct_option = next(o for o in question["options"] if o["is_correct"])
    session = client.post("/api/study-sessions", json={"mode": "RANDOM"}).json()
    client.post(f"/api/study-sessions/{session['id']}/next")

    first = client.post(
        f"/api/study-sessions/{session['id']}/questions/{question['id']}/answer",
        json={"selected_option_id": correct_option["id"]},
    )
    assert first.status_code == 200

    second = client.post(
        f"/api/study-sessions/{session['id']}/questions/{question['id']}/answer",
        json={"selected_option_id": correct_option["id"]},
    )
    assert second.status_code == 422
