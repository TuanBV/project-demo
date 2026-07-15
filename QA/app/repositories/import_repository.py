from __future__ import annotations

from sqlalchemy import select

from app.db.models.import_job import ImportItem, ImportJob
from app.repositories.base import BaseRepository


class ImportRepository(BaseRepository[ImportJob]):
    model = ImportJob

    def list_jobs(self, page: int = 1, page_size: int = 20) -> tuple[list[ImportJob], int]:
        stmt = select(ImportJob).order_by(ImportJob.id.desc())
        total = len(self.db.execute(stmt).scalars().all())
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        items = list(self.db.execute(stmt).scalars().all())
        return items, total

    def add_item(self, item: ImportItem) -> ImportItem:
        self.db.add(item)
        self.db.flush()
        return item
