"""Import every model so Base.metadata is fully populated for Alembic autogenerate."""

from app.db.models.category import Category
from app.db.models.evaluation import AnswerConcept, ConceptKeyword, ContradictionRule
from app.db.models.import_job import ImportItem, ImportJob
from app.db.models.question import Question
from app.db.models.question_delivery import QuestionDelivery
from app.db.models.question_option import QuestionOption
from app.db.models.study import Attempt, QuestionProgress, StudySession

__all__ = [
    "Category",
    "Question",
    "QuestionOption",
    "QuestionDelivery",
    "AnswerConcept",
    "ConceptKeyword",
    "ContradictionRule",
    "ImportJob",
    "ImportItem",
    "StudySession",
    "Attempt",
    "QuestionProgress",
]
