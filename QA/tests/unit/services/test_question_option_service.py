from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import ValidationFailedError
from app.db.models.category import Category
from app.db.models.enums import QuestionFormat, QuestionType, SourceType
from app.db.models.question import Question
from app.services.question_option_service import OptionInput, QuestionOptionService

service = QuestionOptionService()


def _options(
    correct: str = "Máy ảo thực thi Java bytecode.",
    wrong: tuple[str, str, str] = ("Trình biên dịch.", "Framework giao diện.", "Hệ quản trị CSDL."),
) -> list[OptionInput]:
    return [
        OptionInput(content=correct, is_correct=True),
        OptionInput(content=wrong[0], is_correct=False),
        OptionInput(content=wrong[1], is_correct=False),
        OptionInput(content=wrong[2], is_correct=False),
    ]


def test_exactly_four_options_succeeds() -> None:
    built = service.validate_and_build(_options())
    assert len(built) == 4
    assert sum(1 for o in built if o.is_correct) == 1


def test_three_options_rejected() -> None:
    with pytest.raises(ValidationFailedError):
        service.validate_and_build(_options()[:3])


def test_five_options_rejected() -> None:
    extra = _options() + [OptionInput(content="Thêm một đáp án nữa.", is_correct=False)]
    with pytest.raises(ValidationFailedError):
        service.validate_and_build(extra)


def test_no_correct_answer_rejected() -> None:
    opts = _options()
    opts[0] = OptionInput(content=opts[0].content, is_correct=False)
    with pytest.raises(ValidationFailedError):
        service.validate_and_build(opts)


def test_two_correct_answers_rejected() -> None:
    opts = _options()
    opts[1] = OptionInput(content=opts[1].content, is_correct=True)
    with pytest.raises(ValidationFailedError):
        service.validate_and_build(opts)


def test_duplicate_options_rejected() -> None:
    opts = _options()
    opts[1] = OptionInput(content=opts[0].content.upper(), is_correct=False)
    with pytest.raises(ValidationFailedError):
        service.validate_and_build(opts)


def test_empty_option_rejected() -> None:
    opts = _options()
    opts[2] = OptionInput(content="   ", is_correct=False)
    with pytest.raises(ValidationFailedError):
        service.validate_and_build(opts)


def test_display_order_matches_input_order() -> None:
    built = service.validate_and_build(_options())
    assert [o.display_order for o in built] == [0, 1, 2, 3]


def test_replace_options_leaves_question_unchanged_on_invalid_update(db_session: Session) -> None:
    category = Category(name="Option Tx Test", slug="option-tx-test")
    db_session.add(category)
    db_session.flush()
    question = Question(
        category_id=category.id,
        question_type=QuestionType.TEXT,
        question_format=QuestionFormat.MULTIPLE_CHOICE,
        content="Q?",
        content_hash="tx-hash-1",
        source_type=SourceType.MANUAL,
    )
    db_session.add(question)
    db_session.flush()

    service.replace_options(question, _options())
    db_session.flush()
    assert len(question.options) == 4

    bad_options = _options()
    bad_options[1] = OptionInput(content=bad_options[1].content, is_correct=True)
    with pytest.raises(ValidationFailedError):
        service.replace_options(question, bad_options)
    db_session.flush()

    assert len(question.options) == 4
    assert sum(1 for o in question.options if o.is_correct) == 1
