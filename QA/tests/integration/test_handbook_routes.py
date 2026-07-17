"""Integration tests for /handbook/* pages. Uses the plain `TestClient(app)` directly (not
the `client` fixture from conftest.py, which wires up the quiz DB) -- this feature has no
database dependency at all."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.handbook.store import DOCX_PATH
from app.main import app

pytestmark = pytest.mark.skipif(
    not DOCX_PATH.exists(), reason="scripts/data/so_tay_on_tap_de_doc_noi_bat.docx missing"
)


@pytest.fixture()
def hb_client() -> TestClient:
    return TestClient(app)


def test_overview_page_returns_200(hb_client: TestClient) -> None:
    response = hb_client.get("/handbook")
    assert response.status_code == 200
    assert "Sổ tay ôn tập" in response.text
    assert 'href="/handbook/topics/oop-solid"' in response.text


def test_topic_page_returns_200_with_full_content(hb_client: TestClient) -> None:
    response = hb_client.get("/handbook/topics/oop-solid")
    assert response.status_code == 200
    html = response.text
    for expected in (
        "hb-goal-box",
        "hb-terms-table",
        "hb-mistakes-box",
        "hb-example-block",
        "hb-qa-card",
        'id="cau-1"',
    ):
        assert expected in html


def test_topic_page_returns_404_for_invalid_slug(hb_client: TestClient) -> None:
    response = hb_client.get("/handbook/topics/does-not-exist")
    assert response.status_code == 404


def test_glossary_page_returns_200(hb_client: TestClient) -> None:
    response = hb_client.get("/handbook/glossary")
    assert response.status_code == 200
    assert "hb-terms-table" in response.text


def test_handbook_pages_have_no_js_dependency(hb_client: TestClient) -> None:
    for path in ("/handbook", "/handbook/topics/oop-solid", "/handbook/glossary"):
        html = hb_client.get(path).text
        assert "/static/js/study.js" not in html
        assert "/static/js/practical_review.js" not in html


# --- Existing app must still work -------------------------------------------------------


def test_existing_quiz_and_practical_review_routes_are_unaffected(client: TestClient) -> None:
    assert client.get("/").status_code == 200
    assert client.get("/study").status_code == 200
    assert client.get("/api/categories").status_code == 200
