"""Tests for app/practical_review/store.py -- search, lookup, and the isolation guard that
proves this module never imports the quiz feature or the JSON seed data."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.practical_review.store import DOCX_PATH, get_store

pytestmark = pytest.mark.skipif(
    not DOCX_PATH.exists(), reason="scripts/data/bo_cau_hoi_thuc_chien_java_python.docx missing"
)


@pytest.fixture(scope="module")
def store():  # type: ignore[no-untyped-def]
    return get_store()


def test_get_store_is_cached_singleton(store) -> None:  # type: ignore[no-untyped-def]
    assert get_store() is store


def test_list_topics_returns_12_in_order(store) -> None:  # type: ignore[no-untyped-def]
    topics = store.list_topics()
    assert len(topics) == 12
    assert [t.order for t in topics] == list(range(1, 13))


def test_get_topic_unknown_slug_returns_none(store) -> None:  # type: ignore[no-untyped-def]
    assert store.get_topic("does-not-exist") is None


def test_list_questions_for_topic_returns_20_sorted(store) -> None:  # type: ignore[no-untyped-def]
    questions = store.list_questions("oop")
    assert len(questions) == 20
    assert [q.number for q in questions] == sorted(q.number for q in questions)


def test_get_question_by_number(store) -> None:  # type: ignore[no-untyped-def]
    question = store.get_question(1)
    assert question is not None
    assert question.number == 1
    assert question.topic_slug == "oop"


def test_get_question_unknown_number_returns_none(store) -> None:  # type: ignore[no-untyped-def]
    assert store.get_question(99999) is None


def test_search_is_case_insensitive(store) -> None:  # type: ignore[no-untyped-def]
    lower = store.search("encapsulation")
    upper = store.search("ENCAPSULATION")
    assert len(lower) == len(upper) > 0


def test_search_finds_vietnamese_with_diacritics(store) -> None:  # type: ignore[no-untyped-def]
    results = store.search("đối tượng")
    assert len(results) > 0


def test_search_finds_vietnamese_without_diacritics(store) -> None:  # type: ignore[no-untyped-def]
    with_marks = store.search("đối tượng")
    without_marks = store.search("doi tuong")
    assert len(without_marks) > 0
    assert len(without_marks) == len(with_marks)


def test_search_scoped_to_topic(store) -> None:  # type: ignore[no-untyped-def]
    all_results = store.search("là gì")
    scoped_results = store.search("là gì", topic_slug="oop")
    assert len(scoped_results) <= len(all_results)
    assert all(r.topic_slug == "oop" for r in scoped_results)


def test_search_empty_query_returns_nothing(store) -> None:  # type: ignore[no-untyped-def]
    assert store.search("") == []
    assert store.search("   ") == []


def test_source_display_path_is_relative_to_docx(store) -> None:  # type: ignore[no-untyped-def]
    assert store.source_display_path == "scripts/data/bo_cau_hoi_thuc_chien_java_python.docx"


class TestIsolationGuard:
    """Static-analysis guard: no file under app/practical_review/ may import or read
    scripts/data/java_python_mc, scripts/data/extended_topics, or the quiz DB models."""

    FORBIDDEN_SUBSTRINGS = (
        "java_python_mc",
        "extended_topics",
        "app.db.models.question",
        "app.db.models.study",
        "app.services.question_service",
        "app.services.study_service",
    )

    def _module_files(self) -> list[Path]:
        package_dir = Path(__file__).resolve().parents[3] / "app" / "practical_review"
        return sorted(package_dir.glob("*.py"))

    @staticmethod
    def _non_docstring_string_constants(tree: ast.AST) -> list[str]:
        """Every string literal in the module EXCEPT docstrings -- so prose explaining what
        NOT to depend on (in a module/function docstring) doesn't trip this guard, while any
        real path/import-like string literal used in code still would."""
        docstring_ids = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    docstring_ids.add(id(node.body[0].value))
        return [
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and id(node) not in docstring_ids
        ]

    def test_no_module_references_forbidden_data_sources(self) -> None:
        for path in self._module_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for value in self._non_docstring_string_constants(tree):
                for forbidden in self.FORBIDDEN_SUBSTRINGS:
                    assert forbidden not in value, (
                        f"{path} references forbidden {forbidden!r} in literal {value!r}"
                    )

    def test_no_module_imports_sqlalchemy_or_quiz_schemas(self) -> None:
        for path in self._module_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert not alias.name.startswith("sqlalchemy"), (
                            f"{path} imports sqlalchemy directly: {alias.name}"
                        )
                elif isinstance(node, ast.ImportFrom) and node.module:
                    assert not node.module.startswith("sqlalchemy"), (
                        f"{path} imports from sqlalchemy: {node.module}"
                    )
                    assert node.module not in {
                        "app.schemas.question",
                        "app.schemas.study",
                        "app.db.models.question",
                        "app.db.models.study",
                    }, f"{path} imports quiz-specific module: {node.module}"
