"""Tests for app/handbook/store.py -- lookup and the isolation guard that proves this module
never imports the quiz feature, the JSON seed data, or app/practical_review/*."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.handbook.store import DOCX_PATH, get_store

pytestmark = pytest.mark.skipif(
    not DOCX_PATH.exists(), reason="scripts/data/so_tay_on_tap_de_doc_noi_bat.docx missing"
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


def test_get_topic_returns_full_content(store) -> None:  # type: ignore[no-untyped-def]
    topic = store.get_topic("oop-solid")
    assert topic is not None
    assert topic.question_count == 20
    assert topic.goal
    assert topic.terms
    assert topic.common_mistakes


def test_list_glossary_returns_appendix_terms(store) -> None:  # type: ignore[no-untyped-def]
    terms = store.list_glossary()
    assert len(terms) > 0


def test_question_and_topic_counts(store) -> None:  # type: ignore[no-untyped-def]
    assert store.topic_count == 12
    assert store.question_count == 240


def test_source_display_path_is_relative_to_docx(store) -> None:  # type: ignore[no-untyped-def]
    assert store.source_display_path == "scripts/data/so_tay_on_tap_de_doc_noi_bat.docx"


class TestIsolationGuard:
    """Static-analysis guard: no file under app/handbook/ may import or read
    scripts/data/java_python_mc, scripts/data/extended_topics, the quiz DB models, or
    app.practical_review."""

    FORBIDDEN_SUBSTRINGS = (
        "java_python_mc",
        "extended_topics",
        "app.db.models.question",
        "app.db.models.study",
        "app.services.question_service",
        "app.services.study_service",
        "app.practical_review",
    )

    def _module_files(self) -> list[Path]:
        package_dir = Path(__file__).resolve().parents[3] / "app" / "handbook"
        return sorted(package_dir.glob("*.py"))

    @staticmethod
    def _non_docstring_string_constants(tree: ast.AST) -> list[str]:
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

    def test_no_module_imports_sqlalchemy_or_forbidden_modules(self) -> None:
        for path in self._module_files():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert not alias.name.startswith("sqlalchemy"), (
                            f"{path} imports sqlalchemy directly: {alias.name}"
                        )
                        assert not alias.name.startswith("app.practical_review"), (
                            f"{path} imports app.practical_review: {alias.name}"
                        )
                elif isinstance(node, ast.ImportFrom) and node.module:
                    assert not node.module.startswith("sqlalchemy"), (
                        f"{path} imports from sqlalchemy: {node.module}"
                    )
                    assert not node.module.startswith("app.practical_review"), (
                        f"{path} imports from app.practical_review: {node.module}"
                    )
                    assert node.module not in {
                        "app.schemas.question",
                        "app.schemas.study",
                        "app.db.models.question",
                        "app.db.models.study",
                    }, f"{path} imports quiz-specific module: {node.module}"
