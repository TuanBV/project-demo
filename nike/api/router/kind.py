from fastapi import APIRouter, Depends
from schema.kind import KindRequest, KindResponse, ListKindResponse
from kind import KindService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import ok
from helpers import context
from dependencies import authorized_user
from router.common import CommonRoute
from utils.kbn import ROLE
from decorators import permission

kind_router = APIRouter(route_class=CommonRoute, prefix='/kind', tags=['kind'],
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

@kind_router.get('', responses={200:{"model": Response[ListKindResponse]}})
@inject
def get_all(kind_service: KindService = Depends(Provide(Container.kind_service))):
    """
        Get list kind
    """
    data = kind_service.get_all()
    payload = ListKindResponse(**data)
    response = ok(data=payload.dict())
    return response

@kind_router.post('', tags=["kind"], responses={200: {"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def add(request: KindRequest,
        kind_service: KindService = Depends(Provide(Container.kind_service))):
    """
        Add kind
    """
    kind_service.add(request.name, context.user.value["username"])
    return ok()

@kind_router.get('/{kind_id}', responses={200:{"model": Response[KindResponse]}})
@inject
def get_by_kind_id(kind_id: int,
        kind_service: KindService = Depends(Provide(Container.kind_service))):
    """
        Get list kind
    """
    data = kind_service.get_by_kind_id(kind_id)
    payload = KindResponse(**data)
    response = ok(data=payload.__dict__)
    return response

@kind_router.put('/{kind_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def update_kind(kind_id: int,
        request: KindRequest,
        kind_service: KindService = Depends(Provide(Container.kind_service))):
    """
        Update kind
    """
    kind_service.update(kind_id, request.__dict__["name"], context.user.value["username"])
    return ok()

@kind_router.delete('/{kind_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def delete_kind(kind_id: int,
        kind_service: KindService = Depends(Provide(Container.kind_service))):
    """
        Delete kind
    """
    kind_service.delete(kind_id, context.user.value["username"])
    return ok()

@kind_router.put('/{kind_id}/active', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def active_kind(kind_id: int,
        kind_service: KindService = Depends(Provide(Container.kind_service))):
    """
        Active kind
    """
    kind_service.active(kind_id, context.user.value["username"])
    return ok()
