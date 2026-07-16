"""Read-only knowledge-review endpoint (GET /api/knowledge-review): deliberately reveals the
correct answer for browsing/studying -- the opposite invariant of the quiz-facing
StudyQuestionResponse, so covered separately here rather than mixed into
test_api_contracts.py's answer-leak assertions."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_mc_question(client: TestClient, category_name: str = "Review MC Cat") -> dict:
    category = client.post("/api/admin/categories", json={"name": category_name}).json()
    question = client.post(
        "/api/admin/questions",
        json={
            "category_id": category["id"],
            "content": "JVM la gi?",
            "explanation": "JVM thuc thi Java bytecode.",
            "options": [
                {"content": "May ao thuc thi Java bytecode.", "is_correct": True},
                {"content": "Trinh bien dich.", "is_correct": False},
                {"content": "Thu vien giao dien.", "is_correct": False},
                {"content": "He quan tri CSDL.", "is_correct": False},
            ],
        },
    ).json()
    return {"category": category, "question": question}


def test_knowledge_review_includes_correct_answer_and_explanation(client: TestClient) -> None:
    ctx = _create_mc_question(client)
    response = client.get("/api/knowledge-review")
    assert response.status_code == 200
    body = response.json()

    item = next(i for i in body["items"] if i["id"] == ctx["question"]["id"])
    assert item["correct_answer"] == "May ao thuc thi Java bytecode."
    assert item["explanation"] == "JVM thuc thi Java bytecode."
    assert set(item["options"]) == {
        "May ao thuc thi Java bytecode.",
        "Trinh bien dich.",
        "Thu vien giao dien.",
        "He quan tri CSDL.",
    }
    assert item["category"]["name"] == ctx["category"]["name"]


def test_knowledge_review_filters_by_category(client: TestClient) -> None:
    ctx_a = _create_mc_question(client, category_name="Review Cat A")
    _create_mc_question(client, category_name="Review Cat B")

    response = client.get(f"/api/knowledge-review?category_id={ctx_a['category']['id']}")
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["category"]["name"] == "Review Cat A"


def test_knowledge_review_excludes_needs_review_questions(client: TestClient) -> None:
    category = client.post("/api/admin/categories", json={"name": "Review Pending Cat"}).json()
    content = f"CATEGORY: {category['name']}\nQUESTION: Cau hoi chua duyet?\nANSWER: Dap an mau.\n"
    result = client.post("/api/admin/import/text", json={"content": content})
    assert result.status_code == 200
    job = result.json()
    assert job["summary"]["questions_needs_review"] >= 1

    response = client.get(f"/api/knowledge-review?category_id={category['id']}")
    body = response.json()
    assert body["total"] == 0


def test_knowledge_review_pagination(client: TestClient) -> None:
    category_name = "Review Pagination Cat"
    for i in range(3):
        _create_mc_question(client, category_name=f"{category_name} {i}")

    response = client.get("/api/knowledge-review?page=1&page_size=2")
    body = response.json()
    assert len(body["items"]) == 2
    assert body["page"] == 1
    assert body["page_size"] == 2
    assert body["total"] >= 3
