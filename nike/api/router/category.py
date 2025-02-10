from fastapi import APIRouter, Depends
from schema.category import CategoryRequest, CategoryResponse, ListCategoryResponse
from category import CategoryService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import ok
from helpers import context
from dependencies import authorized_user
from router.common import CommonRoute
from utils.kbn import ROLE
from decorators import permission
# from fastapi.encoders import jsonable_encoder

category_router = APIRouter(route_class=CommonRoute, prefix='/category', tags=['category'],
    responses={
        200: {
            "model": Response
        },
        401: {
            "model": Response[dict]
        },
        404: {
            "description": "No data",
            "model": Response[dict]
        },
        400: {
            "description": "API ERROR",
            "model": Response[dict]
        },
        500: {
            "description": "SYSTEM ERROR",
            "model": Response[dict]
        },
    },
)

@category_router.get('', responses={200:{"model": Response[ListCategoryResponse]}})
@inject
def get_all(category_service: CategoryService = Depends(Provide(Container.category_service))):
    """
        Get list category
    """
    data = category_service.get_all()
    payload = ListCategoryResponse(**data)
    response = ok(data=payload.dict())
    return response

@category_router.post('', tags=["category"], responses={200: {"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def add(request: CategoryRequest,
        category_service: CategoryService = Depends(Provide(Container.category_service))):
    """
        Add category
    """
    category_service.add(request.name, context.user.value["username"])
    return ok()

@category_router.get('/{category_id}', responses={200:{"model": Response[CategoryResponse]}})
@inject
def get_by_category_id(category_id: int,
        category_service: CategoryService = Depends(Provide(Container.category_service))):
    """
        Get list category
    """
    data = category_service.get_by_category_id(category_id)
    payload = CategoryResponse(**data)
    response = ok(data=payload.__dict__)
    return response

@category_router.put('/{category_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def update_category(category_id: int,
        request: CategoryRequest,
        category_service: CategoryService = Depends(Provide(Container.category_service))):
    """
        Update category
    """
    category_service.update(category_id, request.__dict__["name"], context.user.value["username"])
    return ok()

@category_router.delete('/{category_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def delete_category(category_id: int,
        category_service: CategoryService = Depends(Provide(Container.category_service))):
    """
        Delete category
    """
    category_service.delete(category_id, context.user.value["username"])
    return ok()

@category_router.put('/{category_id}/active', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def active_category(category_id: int,
        category_service: CategoryService = Depends(Provide(Container.category_service))):
    """
        Active category
    """
    category_service.active(category_id, context.user.value["username"])
    return ok()
