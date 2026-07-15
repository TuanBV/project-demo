from __future__ import annotations

from app.importers.distractor_quality_validator import DistractorQualityValidator

validator = DistractorQualityValidator()


def test_no_warnings_for_well_balanced_options() -> None:
    warnings = validator.validate(
        "May ao thuc thi Java bytecode.",
        [
            "Trinh bien dich source code Java.",
            "Thu vien giao dien nguoi dung.",
            "He quan tri CSDL.",
        ],
    )
    assert warnings == []


def test_generic_catch_all_flagged() -> None:
    warnings = validator.validate(
        "May ao thuc thi Java bytecode.",
        ["Tat ca dap an tren", "Thu vien giao dien nguoi dung.", "He quan tri CSDL."],
    )
    assert any("chung chung" in w for w in warnings)


def test_distractor_much_shorter_flagged() -> None:
    warnings = validator.validate(
        "May ao thuc thi Java bytecode voi nhieu tinh nang toi uu hoa hieu suat.",
        ["A", "Thu vien giao dien nguoi dung cua Java co nhieu thanh phan.", "He quan tri CSDL."],
    )
    assert any("ngắn hơn" in w for w in warnings)


def test_distractor_containing_full_correct_answer_flagged() -> None:
    warnings = validator.validate(
        "May ao thuc thi Java bytecode.",
        [
            "May ao thuc thi Java bytecode va them nhieu thu khac nua.",
            "Thu vien giao dien.",
            "He quan tri CSDL.",
        ],
    )
    assert any("chứa toàn bộ đáp án đúng" in w for w in warnings)


def test_duplicate_distractors_flagged() -> None:
    warnings = validator.validate(
        "Dap an dung.",
        ["Dap an sai.", "Dap an sai.", "Dap an khac."],
    )
    assert any("trùng nội dung" in w for w in warnings)
