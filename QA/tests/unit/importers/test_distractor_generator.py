from __future__ import annotations

from app.importers.distractor_generator import (
    RuleBasedDistractorGenerator,
    is_placeholder_distractor,
)

generator = RuleBasedDistractorGenerator()


def test_confusable_term_swap_produces_distinct_distractor() -> None:
    distractors = generator.generate(
        "Compiler la gi?", "Compiler dich toan bo ma nguon truoc khi chay.", count=3
    )
    assert len(distractors) == 3
    assert distractors[0] != "Compiler dich toan bo ma nguon truoc khi chay."
    assert "interpreter" in distractors[0].lower()


def test_sibling_context_used_as_distractors() -> None:
    context = ["Interpreter dich va chay tung dong lenh.", "Mutable co the thay doi."]
    distractors = generator.generate(
        "Compiler la gi?", "Compiler dich toan bo ma nguon.", context=context, count=3
    )
    assert "Interpreter dich va chay tung dong lenh." in distractors
    assert "Mutable co the thay doi." in distractors


def test_falls_back_to_placeholder_when_no_strategy_available() -> None:
    distractors = generator.generate(
        "Q?", "Mot cau tra loi khong co thuat ngu quen thuoc.", count=3
    )
    assert len(distractors) == 3
    assert any(is_placeholder_distractor(d) for d in distractors)


def test_no_duplicate_distractors_generated() -> None:
    context = [
        "Interpreter dich va chay tung dong lenh.",
        "Interpreter dich va chay tung dong lenh.",
    ]
    distractors = generator.generate(
        "Compiler la gi?", "Compiler dich toan bo ma nguon.", context=context, count=3
    )
    assert len(distractors) == len(set(distractors))
