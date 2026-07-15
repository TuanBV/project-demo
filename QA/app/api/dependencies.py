"""Shared FastAPI dependencies (DB session, repositories, services)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.evaluation.keyword_evaluator import KeywordAnswerEvaluator
from app.repositories.category_repository import CategoryRepository
from app.repositories.import_repository import ImportRepository
from app.repositories.question_repository import QuestionRepository
from app.repositories.study_repository import StudyRepository
from app.services.category_service import CategoryService
from app.services.evaluation_service import EvaluationService
from app.services.import_service import QuestionImportService
from app.services.progress_service import ProgressService
from app.services.question_service import QuestionService
from app.services.study_service import StudyService


def category_service(db: Session) -> CategoryService:
    return CategoryService(CategoryRepository(db))


def question_service(db: Session) -> QuestionService:
    return QuestionService(QuestionRepository(db), CategoryRepository(db))


def evaluation_service(db: Session) -> EvaluationService:
    return EvaluationService(QuestionRepository(db), KeywordAnswerEvaluator())


def import_service(db: Session) -> QuestionImportService:
    return QuestionImportService(
        db=db,
        question_repository=QuestionRepository(db),
        category_repository=CategoryRepository(db),
        import_repository=ImportRepository(db),
    )


def study_service(db: Session) -> StudyService:
    return StudyService(
        StudyRepository(db),
        QuestionRepository(db),
        KeywordAnswerEvaluator(),
    )


def progress_service(db: Session) -> ProgressService:
    return ProgressService(StudyRepository(db), QuestionRepository(db), CategoryRepository(db))


__all__ = [
    "get_db",
    "category_service",
    "question_service",
    "evaluation_service",
    "import_service",
    "study_service",
    "progress_service",
]
