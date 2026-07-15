"""QuestionOptionService: enforces the 4-option / 1-correct invariant transactionally.

This is the single place that decides whether a set of options is structurally valid for
a MULTIPLE_CHOICE question (spec section 4.2/5). Quality (are the wrong answers plausible?)
is a separate, softer concern handled by DistractorQualityValidator -- this service only
blocks clearly broken data (wrong count, wrong number of correct answers, empty/duplicate
content), matching "Không chỉ kiểm tra ở frontend... Database constraint ở mức hợp lý."
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session as OrmSession

from app.core.config import get_settings
from app.core.exceptions import ValidationFailedError
from app.db.models.question import Question
from app.db.models.question_option import QuestionOption
from app.evaluation.normalizer import TextNormalizer


@dataclass(frozen=True)
class OptionInput:
    content: str
    is_correct: bool
    explanation: str | None = None
    auto_generated: bool = False


class QuestionOptionService:
    def __init__(self, normalizer: TextNormalizer | None = None) -> None:
        self._normalizer = normalizer or TextNormalizer()
        self._settings = get_settings()

    def normalize(self, content: str) -> str:
        return self._normalizer.normalize(content).without_diacritics

    def validate_and_build(self, options: list[OptionInput]) -> list[QuestionOption]:
        required_count = self._settings.multiple_choice_option_count
        required_correct = self._settings.multiple_choice_correct_option_count

        if len(options) != required_count:
            raise ValidationFailedError(
                f"Phải có đúng {required_count} đáp án, hiện có {len(options)}"
            )

        correct_options = [o for o in options if o.is_correct]
        if len(correct_options) != required_correct:
            raise ValidationFailedError(
                f"Phải có đúng {required_correct} đáp án đúng, hiện có {len(correct_options)}"
            )

        built: list[QuestionOption] = []
        seen_normalized: set[str] = set()
        for index, option in enumerate(options):
            content = option.content.strip()
            if not content:
                raise ValidationFailedError("Đáp án không được để trống")

            normalized = self.normalize(content)
            if not normalized:
                raise ValidationFailedError("Đáp án không được để trống")
            if normalized in seen_normalized:
                raise ValidationFailedError(f"Các đáp án không được trùng nhau: '{content}'")
            seen_normalized.add(normalized)

            built.append(
                QuestionOption(
                    content=content,
                    normalized_content=normalized,
                    is_correct=option.is_correct,
                    auto_generated=option.auto_generated,
                    explanation=option.explanation,
                    display_order=index,
                    active=True,
                )
            )
        return built

    def replace_options(self, question: Question, options: list[OptionInput]) -> None:
        """Validate first (raises before any mutation), then swap the option set.

        Flushes right after clearing so the delete-orphan DELETEs for the old options
        are issued before the new INSERTs -- otherwise SQLAlchemy may order the new
        is_correct=1 row's INSERT before the old row's DELETE within the same flush,
        tripping the partial unique index (at most one correct option per question).
        """
        built = self.validate_and_build(options)
        question.options.clear()
        session = OrmSession.object_session(question)
        if session is not None:
            session.flush()
        for option in built:
            question.options.append(option)
