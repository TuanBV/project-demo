"""Tests for scripts/extract_practical_review_docx.py -- loaded via importlib since scripts/
isn't a package (matches the pattern used for other CLI scripts, e.g.
tests/unit/scripts/test_seed_java_python_mc.py)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from app.practical_review.store import DOCX_PATH

pytestmark = pytest.mark.skipif(
    not DOCX_PATH.exists(), reason="scripts/data/bo_cau_hoi_thuc_chien_java_python.docx missing"
)

_MODULE_PATH = Path(__file__).resolve().parents[3] / "scripts" / "extract_practical_review_docx.py"
_spec = importlib.util.spec_from_file_location("extract_practical_review_docx", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
extract_script = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(extract_script)


def test_build_report_mentions_all_12_topics() -> None:
    from app.practical_review.docx_parser import parse_docx

    document = parse_docx(DOCX_PATH)
    report = extract_script.build_report(document)
    report_text = "\n".join(report)
    assert "Tổng số chủ đề: 12" in report_text
    assert "Tổng số câu hỏi: 240" in report_text
    for topic in document.topics:
        assert topic.display_name in report_text


def test_generated_payload_has_required_metadata_header() -> None:
    from app.practical_review.docx_parser import parse_docx

    document = parse_docx(DOCX_PATH)
    payload = extract_script.to_generated_payload(document)
    assert payload["source"] == "scripts/data/bo_cau_hoi_thuc_chien_java_python.docx"
    assert payload["topic_count"] == 12
    assert payload["question_count"] == 240
    assert len(payload["topics"]) == 12
    assert len(payload["questions"]) == 240
    assert "generated_at" in payload


def test_payload_is_deterministic_across_runs_except_timestamp() -> None:
    from app.practical_review.docx_parser import parse_docx

    document_a = parse_docx(DOCX_PATH)
    document_b = parse_docx(DOCX_PATH)
    payload_a = extract_script.to_generated_payload(document_a)
    payload_b = extract_script.to_generated_payload(document_b)
    payload_a.pop("generated_at")
    payload_b.pop("generated_at")
    assert payload_a == payload_b


def test_payload_is_json_serializable_with_vietnamese_text(tmp_path: Path) -> None:
    from app.practical_review.docx_parser import parse_docx

    document = parse_docx(DOCX_PATH)
    payload = extract_script.to_generated_payload(document)
    out_path = tmp_path / "questions.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    reloaded = json.loads(out_path.read_text(encoding="utf-8"))
    assert reloaded["questions"][0]["question"] == document.questions[0].question


def test_main_check_only_does_not_write_generated_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_generated_dir = tmp_path / "generated"
    monkeypatch.setattr(extract_script, "GENERATED_DIR", fake_generated_dir)
    monkeypatch.setattr(extract_script, "GENERATED_PATH", fake_generated_dir / "questions.json")
    monkeypatch.setattr("sys.argv", ["extract_practical_review_docx.py", "--check-only"])
    exit_code = extract_script.main()
    assert exit_code == 0
    assert not fake_generated_dir.exists()


def test_main_writes_generated_file_by_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake_generated_dir = tmp_path / "generated"
    fake_generated_path = fake_generated_dir / "questions.json"
    monkeypatch.setattr(extract_script, "GENERATED_DIR", fake_generated_dir)
    monkeypatch.setattr(extract_script, "GENERATED_PATH", fake_generated_path)
    monkeypatch.setattr("sys.argv", ["extract_practical_review_docx.py"])
    exit_code = extract_script.main()
    assert exit_code == 0
    assert fake_generated_path.exists()
    payload = json.loads(fake_generated_path.read_text(encoding="utf-8"))
    assert payload["question_count"] == 240
