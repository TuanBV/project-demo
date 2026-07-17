"""Integration tests for /practical-review/* pages and /api/practical-review/* endpoints.
Uses the plain `TestClient(app)` directly (not the `client` fixture from conftest.py, which
wires up the quiz DB) -- this feature has no database dependency at all."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.practical_review.store import DOCX_PATH

pytestmark = pytest.mark.skipif(
    not DOCX_PATH.exists(),
    reason="scripts/data/so_tay_on_tap_sap_xep_theo_chu_de_uu_tien.docx missing",
)


@pytest.fixture()
def pr_client() -> TestClient:
    return TestClient(app)


# --- API: topics -----------------------------------------------------------------------


def test_list_topics_returns_11(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/topics")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 11
    assert sum(t["question_count"] for t in body) == 207


def test_get_valid_topic_returns_200_with_20_questions(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/topics/oop-solid")
    assert response.status_code == 200
    body = response.json()
    assert body["topic"]["slug"] == "oop-solid"
    assert len(body["questions"]) == 20


def test_get_invalid_topic_returns_404(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/topics/does-not-exist")
    assert response.status_code == 404


# --- API: questions ----------------------------------------------------------------------


def test_get_valid_question_returns_200(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/questions/1")
    assert response.status_code == 200
    body = response.json()
    assert body["number"] == 1
    assert body["answer"]
    assert body["explanation"]


def test_get_invalid_question_returns_404(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/questions/99999")
    assert response.status_code == 404


# --- API: search -------------------------------------------------------------------------


def test_search_returns_results(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/search", params={"q": "encapsulation"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] > 0
    assert len(body["items"]) == body["total"]


def test_search_empty_query_returns_empty(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/search", params={"q": ""})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_search_with_invalid_topic_filter_returns_404(pr_client: TestClient) -> None:
    response = pr_client.get(
        "/api/practical-review/search", params={"q": "test", "topic_slug": "nope"}
    )
    assert response.status_code == 404


# --- API: source-info ----------------------------------------------------------------------


def test_source_info_points_to_docx(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/source-info")
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "scripts/data/so_tay_on_tap_sap_xep_theo_chu_de_uu_tien.docx"
    assert body["topic_count"] == 11
    assert body["question_count"] == 207


# --- API: glossary -----------------------------------------------------------------------


def test_glossary_returns_terms_with_definitions(pr_client: TestClient) -> None:
    response = pr_client.get("/api/practical-review/glossary")
    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0
    assert all(entry["term"] and entry["definition"] for entry in body)
    terms = {entry["term"].lower() for entry in body}
    assert "encapsulation" in terms


# --- Web pages ---------------------------------------------------------------------------


def test_overview_page_returns_200(pr_client: TestClient) -> None:
    response = pr_client.get("/practical-review")
    assert response.status_code == 200
    assert 'data-pr-page="overview"' in response.text


def test_topic_page_returns_200_for_valid_slug(pr_client: TestClient) -> None:
    response = pr_client.get("/practical-review/topics/oop-solid")
    assert response.status_code == 200
    assert 'data-pr-page="topic"' in response.text


def test_topic_page_returns_404_for_invalid_slug(pr_client: TestClient) -> None:
    response = pr_client.get("/practical-review/topics/does-not-exist")
    assert response.status_code == 404


def test_study_page_returns_200_for_valid_slug(pr_client: TestClient) -> None:
    response = pr_client.get("/practical-review/topics/oop-solid/study")
    assert response.status_code == 200
    assert 'data-pr-page="study"' in response.text


def test_study_page_returns_404_for_invalid_slug(pr_client: TestClient) -> None:
    response = pr_client.get("/practical-review/topics/does-not-exist/study")
    assert response.status_code == 404


def test_search_page_returns_200(pr_client: TestClient) -> None:
    response = pr_client.get("/practical-review/search")
    assert response.status_code == 200
    assert 'data-pr-page="search"' in response.text


# --- Existing app must still work -------------------------------------------------------
# Uses the shared `client` fixture from tests/conftest.py (isolated in-memory DB) rather than
# `pr_client`, since these routes DO depend on the quiz database and should be checked
# against the same fixture the rest of the quiz test suite uses -- not the real data/app.db.


def test_existing_quiz_routes_are_unaffected(client: TestClient) -> None:
    assert client.get("/").status_code == 200
    assert client.get("/study").status_code == 200
    assert client.get("/api/categories").status_code == 200
