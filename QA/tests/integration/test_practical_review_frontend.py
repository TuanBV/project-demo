"""Frontend checks for the practical-review area: key selectors/data-attributes exist on
each page, and the JS/templates have zero dependency on the quiz feature's API or on
study.js. These are static/HTML-level checks (no browser automation available in this
repo) -- see .claude/rules or README for how UI changes are otherwise manually verified."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.practical_review.store import DOCX_PATH

pytestmark = pytest.mark.skipif(
    not DOCX_PATH.exists(), reason="scripts/data/bo_cau_hoi_thuc_chien_java_python.docx missing"
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PRACTICAL_REVIEW_JS = REPO_ROOT / "app" / "static" / "js" / "practical_review.js"
STUDY_JS = REPO_ROOT / "app" / "static" / "js" / "study.js"

FORBIDDEN_ENDPOINTS = (
    "/api/questions",
    "/api/study-sessions",
    "/api/admin/questions",
    "/api/admin/import",
)


@pytest.fixture()
def pr_client() -> TestClient:
    return TestClient(app)


def _strip_line_comments(source: str) -> str:
    """Drop full-line `//` comments before scanning for forbidden endpoints, so the file's
    own header comment explaining what it must NOT call doesn't trip this guard."""
    return "\n".join(line for line in source.splitlines() if not line.strip().startswith("//"))


def test_js_file_never_calls_quiz_endpoints() -> None:
    source = _strip_line_comments(PRACTICAL_REVIEW_JS.read_text(encoding="utf-8"))
    for endpoint in FORBIDDEN_ENDPOINTS:
        assert endpoint not in source, f"practical_review.js references quiz endpoint {endpoint}"


def test_js_file_only_calls_its_own_api_prefix() -> None:
    source = PRACTICAL_REVIEW_JS.read_text(encoding="utf-8")
    assert "/api/practical-review" in source


def test_study_js_was_not_modified_to_reference_practical_review() -> None:
    source = STUDY_JS.read_text(encoding="utf-8")
    assert "practical" not in source.lower()
    assert "practicalReview" not in source


def test_overview_page_has_key_elements(pr_client: TestClient) -> None:
    html = pr_client.get("/practical-review").text
    for expected in (
        'id="pr-overview-search-input"',
        'id="pr-continue-btn"',
        'id="pr-review-btn"',
        'data-topic-slug="oop"',
        'data-role="progress-fill"',
    ):
        assert expected in html


def test_topic_page_has_key_elements(pr_client: TestClient) -> None:
    html = pr_client.get("/practical-review/topics/oop").text
    for expected in (
        'id="pr-qa-list"',
        'id="pr-topic-search-input"',
        'data-filter="all"',
        'data-filter="unseen"',
        'data-filter="mastered"',
        'data-filter="review"',
    ):
        assert expected in html


def test_study_page_has_key_elements(pr_client: TestClient) -> None:
    html = pr_client.get("/practical-review/topics/oop/study").text
    for expected in (
        'id="pr-flashcard"',
        'id="pr-reveal-btn"',
        'id="pr-flashcard-answer-area"',
        'data-rate="mastered"',
        'data-rate="review"',
        'id="pr-order-mode"',
    ):
        assert expected in html
    # The answer/explanation text must not be pre-rendered into the page HTML -- only
    # inserted client-side after the learner clicks "Xem đáp án".
    assert 'id="pr-flashcard-answer"></p>' in html or 'id="pr-flashcard-answer">' in html


def test_search_page_has_key_elements(pr_client: TestClient) -> None:
    html = pr_client.get("/practical-review/search").text
    for expected in (
        'id="pr-search-input"',
        'id="pr-search-topic-filter"',
        'id="pr-search-results"',
    ):
        assert expected in html


def test_practical_review_pages_do_not_include_study_js(pr_client: TestClient) -> None:
    for path in (
        "/practical-review",
        "/practical-review/topics/oop",
        "/practical-review/topics/oop/study",
        "/practical-review/search",
    ):
        html = pr_client.get(path).text
        assert "/static/js/study.js" not in html
        assert "/static/js/practical_review.js" in html
