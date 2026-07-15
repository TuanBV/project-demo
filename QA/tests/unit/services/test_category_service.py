from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService


def _service(db: Session) -> CategoryService:
    return CategoryService(CategoryRepository(db))


def test_create_and_get_category(db_session: Session) -> None:
    service = _service(db_session)
    category = service.create(CategoryCreate(name="Java Core"))
    assert category.slug == "java-core"
    fetched = service.get(category.id)
    assert fetched.name == "Java Core"


def test_get_missing_category_raises(db_session: Session) -> None:
    service = _service(db_session)
    with pytest.raises(NotFoundError):
        service.get(999)


def test_get_or_create_by_name_reuses_existing(db_session: Session) -> None:
    service = _service(db_session)
    first = service.get_or_create_by_name("Python Core")
    second = service.get_or_create_by_name("Python Core")
    assert first.id == second.id


def test_update_category(db_session: Session) -> None:
    service = _service(db_session)
    category = service.create(CategoryCreate(name="SQL"))
    updated = service.update(
        category.id, CategoryUpdate(description="Cau hoi ve SQL", active=False)
    )
    assert updated.description == "Cau hoi ve SQL"
    assert updated.active is False


def test_update_name_regenerates_unique_slug(db_session: Session) -> None:
    service = _service(db_session)
    service.create(CategoryCreate(name="Git"))
    category2 = service.create(CategoryCreate(name="Git Basics"))
    updated = service.update(category2.id, CategoryUpdate(name="Git"))
    assert updated.slug != "git"
    assert updated.slug.startswith("git-")


def test_delete_category(db_session: Session) -> None:
    service = _service(db_session)
    category = service.create(CategoryCreate(name="Testing"))
    service.delete(category.id)
    with pytest.raises(NotFoundError):
        service.get(category.id)


def test_list_all_active_only(db_session: Session) -> None:
    service = _service(db_session)
    service.create(CategoryCreate(name="Active Cat", active=True))
    service.create(CategoryCreate(name="Inactive Cat", active=False))
    active = service.list_all(active_only=True)
    all_cats = service.list_all(active_only=False)
    assert len(active) == 1
    assert len(all_cats) == 2
