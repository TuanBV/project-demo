from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import category_service, get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(tags=["categories"])


def _service(db: Session = Depends(get_db)) -> CategoryService:
    return category_service(db)


@router.get("/api/categories", response_model=list[CategoryResponse])
def list_categories(
    active_only: bool = True, service: CategoryService = Depends(_service)
) -> list[CategoryResponse]:
    categories = service.list_all(active_only=active_only)
    return [
        CategoryResponse.model_validate(c, from_attributes=True).model_copy(
            update={"question_count": len(c.questions)}
        )
        for c in categories
    ]


@router.get("/api/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int, service: CategoryService = Depends(_service)
) -> CategoryResponse:
    category = service.get(category_id)
    return CategoryResponse.model_validate(category, from_attributes=True).model_copy(
        update={"question_count": len(category.questions)}
    )


@router.post("/api/admin/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate, service: CategoryService = Depends(_service)
) -> CategoryResponse:
    category = service.create(data)
    return CategoryResponse.model_validate(category, from_attributes=True)


@router.put("/api/admin/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, data: CategoryUpdate, service: CategoryService = Depends(_service)
) -> CategoryResponse:
    category = service.update(category_id, data)
    return CategoryResponse.model_validate(category, from_attributes=True)


@router.delete("/api/admin/categories/{category_id}", status_code=204)
def delete_category(category_id: int, service: CategoryService = Depends(_service)) -> None:
    service.delete(category_id)
