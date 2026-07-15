from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models.enums import StudyMode
from app.db.models.question import Question
from app.evaluation.keyword_evaluator import KeywordAnswerEvaluator
from app.repositories.category_repository import CategoryRepository
from app.repositories.question_repository import QuestionRepository
from app.repositories.study_repository import StudyRepository
from app.schemas.category import CategoryCreate
from app.schemas.question import AdminQuestionCreate
from app.services.category_service import CategoryService
from app.services.question_service import QuestionService
from app.services.study_service import StudyService


def _setup(db: Session) -> tuple[StudyService, QuestionService, CategoryService]:
    study_service = StudyService(
        StudyRepository(db), QuestionRepository(db), KeywordAnswerEvaluator()
    )
    question_service = QuestionService(QuestionRepository(db), CategoryRepository(db))
    category_service = CategoryService(CategoryRepository(db))
    return study_service, question_service, category_service


def _make_question(question_service: QuestionService, category_id: int, content: str) -> Question:
    return question_service.create(
        AdminQuestionCreate(
            category_id=category_id,
            content=content,
            options=[
                {"content": "Dap an dung.", "is_correct": True},
                {"content": "Dap an sai 1.", "is_correct": False},
                {"content": "Dap an sai 2.", "is_correct": False},
                {"content": "Dap an sai 3.", "is_correct": False},
            ],
        )
    )


def _correct_option_id(question: Question) -> int:
    return next(o.id for o in question.options if o.is_correct)


def _wrong_option_id(question: Question) -> int:
    return next(o.id for o in question.options if not o.is_correct)


def test_select_question_review_mode_picks_by_priority(db_session: Session) -> None:
    study_service, question_service, category_service = _setup(db_session)
    category = category_service.create(CategoryCreate(name="Review Cat"))
    for i in range(3):
        _make_question(question_service, category.id, f"Cau hoi so {i}?")

    question = study_service.select_question(category_id=category.id, mode=StudyMode.REVIEW)
    assert question is not None
    assert question.category_id == category.id


def test_select_question_unseen_only_prefers_unattempted(db_session: Session) -> None:
    study_service, question_service, category_service = _setup(db_session)
    category = category_service.create(CategoryCreate(name="Unseen Cat"))
    q1 = _make_question(question_service, category.id, "Da lam roi?")
    q2 = _make_question(question_service, category.id, "Chua lam?")

    session = study_service.start_session(StudyMode.RANDOM, None, None)
    study_service.get_delivered_question(session.id, q1.id)
    study_service.submit_option_answer(session.id, q1.id, _correct_option_id(q1), None)

    picked = study_service.select_question(category_id=category.id, unseen_only=True)
    assert picked is not None
    assert picked.id == q2.id


def test_select_question_weak_only_filters_low_scores(db_session: Session) -> None:
    study_service, question_service, category_service = _setup(db_session)
    category = category_service.create(CategoryCreate(name="Weak Cat"))
    weak_q = _make_question(question_service, category.id, "Cau tra loi sai?")

    session = study_service.start_session(StudyMode.RANDOM, None, None)
    study_service.get_delivered_question(session.id, weak_q.id)
    study_service.submit_option_answer(session.id, weak_q.id, _wrong_option_id(weak_q), None)

    picked = study_service.select_question(category_id=category.id, weak_only=True)
    assert picked is not None
    assert picked.id == weak_q.id


def test_select_question_no_candidates_returns_none(db_session: Session) -> None:
    study_service, _, _ = _setup(db_session)
    result = study_service.select_question(category_id=99999)
    assert result is None


def test_finish_session_sets_finished_at(db_session: Session) -> None:
    study_service, _, _ = _setup(db_session)
    session = study_service.start_session(StudyMode.RANDOM, None, None)
    finished = study_service.finish_session(session.id)
    assert finished.finished_at is not None


def test_submit_option_answer_correct(db_session: Session) -> None:
    study_service, question_service, category_service = _setup(db_session)
    category = category_service.create(CategoryCreate(name="Submit Cat"))
    question = _make_question(question_service, category.id, "Q?")
    session = study_service.start_session(StudyMode.RANDOM, None, None)
    study_service.get_delivered_question(session.id, question.id)

    attempt, correct_option, _, _ = study_service.submit_option_answer(
        session.id, question.id, _correct_option_id(question), 12.5
    )
    assert attempt.is_correct is True
    assert attempt.score == 100.0
    assert correct_option.id == _correct_option_id(question)


def test_submit_option_answer_incorrect(db_session: Session) -> None:
    study_service, question_service, category_service = _setup(db_session)
    category = category_service.create(CategoryCreate(name="Submit Cat 2"))
    question = _make_question(question_service, category.id, "Q?")
    session = study_service.start_session(StudyMode.RANDOM, None, None)
    study_service.get_delivered_question(session.id, question.id)

    attempt, _, _, _ = study_service.submit_option_answer(
        session.id, question.id, _wrong_option_id(question), None
    )
    assert attempt.is_correct is False
    assert attempt.score == 0.0


def test_delivered_question_order_stable_within_session(db_session: Session) -> None:
    study_service, question_service, category_service = _setup(db_session)
    category = category_service.create(CategoryCreate(name="Stable Cat"))
    question = _make_question(question_service, category.id, "Q?")
    session = study_service.start_session(StudyMode.RANDOM, None, None)

    first = study_service.get_delivered_question(session.id, question.id)
    second = study_service.get_delivered_question(session.id, question.id)
    assert [o.id for o in first.ordered_options] == [o.id for o in second.ordered_options]
