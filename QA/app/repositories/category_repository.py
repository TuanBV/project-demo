from __future__ import annotations

from sqlalchemy import select

from app.db.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    model = Category

    def list_all(self, active_only: bool = False) -> list[Category]:
        stmt = select(Category).order_by(Category.display_order, Category.name)
        if active_only:
            stmt = stmt.where(Category.active.is_(True))
        return list(self.db.execute(stmt).scalars().all())

    def get_by_slug(self, slug: str) -> Category | None:
        stmt = select(Category).where(Category.slug == slug)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_name(self, name: str) -> Category | None:
        stmt = select(Category).where(Category.name == name)
        return self.db.execute(stmt).scalar_one_or_none()
