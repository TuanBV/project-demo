from __future__ import annotations

from app.evaluation.base import (
    ConceptData,
    ContradictionRuleData,
    KeywordData,
    QuestionEvaluationData,
)
from app.evaluation.keyword_evaluator import KeywordAnswerEvaluator

evaluator = KeywordAnswerEvaluator()


def _question(
    concepts: list[ConceptData], contradictions: list[ContradictionRuleData] | None = None
) -> QuestionEvaluationData:
    return QuestionEvaluationData(
        question_id=1,
        content="dummy question",
        reference_answer="dummy reference",
        concepts=concepts,
        contradiction_rules=contradictions or [],
        minimum_token_count=4,
    )


def test_exact_keyword_full_credit() -> None:
    q = _question(
        [
            ConceptData(
                1, "c1", "desc", 100, True, [KeywordData("visibility", "visibility", "EXACT")]
            )
        ]
    )
    result = evaluator.evaluate(q, "chu de nay lien quan den visibility trong lap trinh da luong")
    assert result.score == 100.0
    assert result.classification == "CORRECT"


def test_contains_keyword_matches() -> None:
    q = _question(
        [
            ConceptData(
                1,
                "c1",
                "desc",
                100,
                True,
                [KeywordData("garbage collector", "garbage collector", "CONTAINS")],
            )
        ]
    )
    result = evaluator.evaluate(q, "gc con goi la garbage collector trong java tu dong don rac")
    assert result.score == 100.0


def test_word_boundary_short_keyword() -> None:
    q = _question([ConceptData(1, "c1", "desc", 100, True, [KeywordData("is", "is", "CONTAINS")])])
    result = evaluator.evaluate(q, "day la mot cai list rat dai va nhieu phan tu ben trong")
    assert result.score < 100.0


def test_fuzzy_typo_still_recognized() -> None:
    q = _question(
        [
            ConceptData(
                1,
                "c1",
                "desc",
                100,
                True,
                [KeywordData("polymorphism", "polymorphism", "FUZZY", 75)],
            )
        ]
    )
    result = evaluator.evaluate(
        q, "khai niem lien quan toi polymorfism trong lap trinh huong doi tuong"
    )
    assert result.score > 0


def test_fuzzy_below_threshold_no_credit() -> None:
    q = _question(
        [
            ConceptData(
                1,
                "c1",
                "desc",
                100,
                True,
                [KeywordData("polymorphism", "polymorphism", "FUZZY", 90)],
            )
        ]
    )
    result = evaluator.evaluate(q, "cau tra loi nay hoan toan khong lien quan chu de nay ca")
    assert result.score == 0.0


def test_alias_synonym_matches() -> None:
    q = _question(
        [ConceptData(1, "c1", "desc", 100, True, [KeywordData("immutable", "immutable", "ALIAS")])]
    )
    result = evaluator.evaluate(q, "kieu du lieu nay la bat bien khong the thay doi duoc nua")
    assert result.score == 100.0


def test_multiple_keywords_same_concept_no_double_count() -> None:
    q = _question(
        [
            ConceptData(
                1,
                "c1",
                "desc",
                100,
                True,
                [
                    KeywordData("immutable", "immutable", "CONTAINS"),
                    KeywordData("bat bien", "bat bien", "CONTAINS"),
                ],
            )
        ]
    )
    result = evaluator.evaluate(q, "day la mot doi tuong bat bien immutable khong doi duoc")
    assert result.score == 100.0
    assert len(result.matched_concepts) == 1


def test_multiple_concepts_different_weights() -> None:
    q = _question(
        [
            ConceptData(
                1, "c1", "desc1", 70, True, [KeywordData("visibility", "visibility", "CONTAINS")]
            ),
            ConceptData(2, "c2", "desc2", 30, False, [KeywordData("atomic", "atomic", "CONTAINS")]),
        ]
    )
    result = evaluator.evaluate(q, "volatile dam bao visibility cho cac bien duoc chia se")
    assert result.score == 70.0


def test_required_concept_missing() -> None:
    q = _question(
        [
            ConceptData(
                1, "c1", "desc", 100, True, [KeywordData("visibility", "visibility", "EXACT")]
            )
        ]
    )
    result = evaluator.evaluate(q, "cau tra loi nay khong nhac den y quan trong nao ca dau")
    assert result.score == 0.0
    assert len(result.missing_concepts) == 1


def test_optional_concept_missing_still_scores_other_concepts() -> None:
    q = _question(
        [
            ConceptData(
                1, "c1", "desc1", 60, True, [KeywordData("visibility", "visibility", "CONTAINS")]
            ),
            ConceptData(2, "c2", "desc2", 40, False, [KeywordData("atomic", "atomic", "CONTAINS")]),
        ]
    )
    result = evaluator.evaluate(q, "volatile dam bao visibility cho cac thread khac nhau doc")
    assert result.score == 60.0
    assert any(m.name == "c2" for m in result.missing_concepts)


def test_empty_answer_scores_zero() -> None:
    q = _question(
        [
            ConceptData(
                1, "c1", "desc", 100, True, [KeywordData("visibility", "visibility", "EXACT")]
            )
        ]
    )
    result = evaluator.evaluate(q, "")
    assert result.score == 0.0
    assert result.classification == "INCORRECT"


def test_bare_keyword_dump_capped() -> None:
    q = _question(
        [
            ConceptData(
                1, "c1", "desc1", 50, True, [KeywordData("visibility", "visibility", "CONTAINS")]
            ),
            ConceptData(
                2, "c2", "desc2", 50, True, [KeywordData("atomicity", "atomicity", "CONTAINS")]
            ),
        ]
    )
    result = evaluator.evaluate(q, "visibility atomicity")
    assert result.answer_quality_capped is True
    assert result.score <= 85.0


def test_contradiction_penalty_applied() -> None:
    q = _question(
        [ConceptData(1, "c1", "desc", 100, True, [KeywordData("atomic", "atomic", "CONTAINS")])],
        [
            ContradictionRuleData(
                "count++ la atomic",
                "sai lech",
                penalty=30,
                maximum_score=None,
                match_type="CONTAINS",
            )
        ],
    )
    result = evaluator.evaluate(q, "volatile dam bao count++ la atomic luon dung")
    assert len(result.contradictions) == 1
    assert result.score == 70.0


def test_contradiction_maximum_score_cap() -> None:
    q = _question(
        [ConceptData(1, "c1", "desc", 100, True, [KeywordData("atomic", "atomic", "CONTAINS")])],
        [
            ContradictionRuleData(
                "count++ la atomic", "sai lech", penalty=5, maximum_score=40, match_type="CONTAINS"
            )
        ],
    )
    result = evaluator.evaluate(q, "volatile dam bao count++ la atomic luon dung")
    assert result.score <= 40.0


def test_weight_not_summing_to_100_is_normalized() -> None:
    q = _question(
        [
            ConceptData(
                1, "c1", "desc1", 30, True, [KeywordData("visibility", "visibility", "CONTAINS")]
            ),
            ConceptData(2, "c2", "desc2", 30, True, [KeywordData("atomic", "atomic", "CONTAINS")]),
        ]
    )
    result = evaluator.evaluate(q, "cau tra loi de cap ca visibility va atomic day du")
    assert result.score == 100.0


def test_english_answer_for_vietnamese_question() -> None:
    q = _question(
        [
            ConceptData(
                1,
                "c1",
                "desc",
                100,
                True,
                [
                    KeywordData("immutable", "immutable", "CONTAINS"),
                    KeywordData("bat bien", "bat bien", "CONTAINS"),
                ],
            )
        ]
    )
    result = evaluator.evaluate(q, "this object is immutable and cannot be changed after creation")
    assert result.score == 100.0


def test_vietnamese_answer_for_english_keyword() -> None:
    q = _question(
        [ConceptData(1, "c1", "desc", 100, True, [KeywordData("immutable", "immutable", "ALIAS")])]
    )
    result = evaluator.evaluate(q, "doi tuong nay bat bien khong the thay doi sau khi tao")
    assert result.score == 100.0


def test_short_keyword_no_wrong_substring_match() -> None:
    q = _question([ConceptData(1, "c1", "desc", 100, True, [KeywordData("is", "is", "CONTAINS")])])
    result = evaluator.evaluate(q, "chung ta co mot danh sach list cac phan tu can xu ly them")
    assert result.score == 0.0
