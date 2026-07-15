"""Base repository: raw SQLAlchemy query access only, no business rules."""

from __future__ import annotations

from typing import TypeVar

from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseRepository[ModelT]:
    model: type[ModelT]

    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, id_: int) -> ModelT | None:
        return self.db.get(self.model, id_)

    def add(self, instance: ModelT) -> ModelT:
        self.db.add(instance)
        self.db.flush()
        return instance

    def delete(self, instance: ModelT) -> None:
        self.db.delete(instance)
        self.db.flush()

    def commit(self) -> None:
        self.db.commit()
