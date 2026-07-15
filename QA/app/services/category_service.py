from __future__ import annotations

from app.core.exceptions import DuplicateResourceError, NotFoundError
from app.db.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.slug import slugify


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self._repository = repository

    def list_all(self, active_only: bool = False) -> list[Category]:
        return self._repository.list_all(active_only=active_only)

    def get(self, category_id: int) -> Category:
        category = self._repository.get(category_id)
        if category is None:
            raise NotFoundError(f"Category {category_id} not found")
        return category

    def get_or_create_by_name(self, name: str) -> Category:
        existing = self._repository.get_by_name(name)
        if existing:
            return existing
        return self.create(CategoryCreate(name=name))

    def create(self, data: CategoryCreate) -> Category:
        slug = self._unique_slug(data.name)
        category = Category(
            name=data.name,
            slug=slug,
            description=data.description,
            display_order=data.display_order,
            active=data.active,
        )
        category = self._repository.add(category)
        self._repository.commit()
        return category

    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = self.get(category_id)
        if data.name is not None and data.name != category.name:
            category.name = data.name
            category.slug = self._unique_slug(data.name, exclude_id=category.id)
        if data.description is not None:
            category.description = data.description
        if data.display_order is not None:
            category.display_order = data.display_order
        if data.active is not None:
            category.active = data.active
        self._repository.commit()
        return category

    def delete(self, category_id: int) -> None:
        category = self.get(category_id)
        self._repository.delete(category)
        self._repository.commit()

    def _unique_slug(self, name: str, exclude_id: int | None = None) -> str:
        base = slugify(name)
        slug = base
        suffix = 2
        while True:
            existing = self._repository.get_by_slug(slug)
            if existing is None or existing.id == exclude_id:
                return slug
            slug = f"{base}-{suffix}"
            suffix += 1
            if suffix > 1000:
                raise DuplicateResourceError("Unable to generate a unique slug")
