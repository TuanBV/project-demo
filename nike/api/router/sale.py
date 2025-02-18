from fastapi import APIRouter, Depends
from schema.sale import SaleRequest, SaleResponse, ListSaleResponse
from sale import SaleService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import ok
from helpers import context
from dependencies import authorized_user
from router.common import CommonRoute
from utils.kbn import ROLE
from decorators import permission

sale_router = APIRouter(route_class=CommonRoute, prefix='/sale', tags=['sale'],
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

@sale_router.get('', responses={200:{"model": Response[ListSaleResponse]}})
@inject
def get_all(sale_service: SaleService = Depends(Provide(Container.sale_service))):
    """
        Get list sale
    """
    data = sale_service.get_all()
    payload = ListSaleResponse(**data)
    response = ok(data=payload.dict())
    return response


@sale_router.post('', tags=["sale"], responses={200: {"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def add(request: SaleRequest,
        sale_service: SaleService = Depends(Provide(Container.sale_service))):
    """
        Add sale
    """
    sale_service.add(request.__dict__, context.user.value["username"])
    return ok()

@sale_router.get('/{sale_id}', responses={200:{"model": Response[SaleResponse]}})
@inject
def get_by_sale_id(sale_id: int,
        sale_service: SaleService = Depends(Provide(Container.sale_service))):
    """
        Get list sale
    """
    data = sale_service.get_by_sale_id(sale_id)
    payload = SaleResponse(**data)
    response = ok(data=payload.__dict__)
    return response

@sale_router.put('/{sale_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def update_sale(sale_id: int,
        request: SaleRequest,
        sale_service: SaleService = Depends(Provide(Container.sale_service))):
    """
        Update sale
    """
    sale_service.update(sale_id, request.__dict__, context.user.value["username"])
    return ok()

@sale_router.delete('/{sale_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def delete_sale(sale_id: int,
        sale_service: SaleService = Depends(Provide(Container.sale_service))):
    """
        Delete sale
    """
    sale_service.delete(sale_id, context.user.value["username"])
    return ok()

@sale_router.put('/{sale_id}/active', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def active_sale(sale_id: int,
        sale_service: SaleService = Depends(Provide(Container.sale_service))):
    """
        Active sale
    """
    sale_service.active(sale_id, context.user.value["username"])
    return ok()
