from fastapi import APIRouter, Depends
# from schema.product import ProductRequest, ProductResponse, ListProductResponse
from schema.product import ProductRequest, ListProductResponse
from product import ProductService
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

product_router = APIRouter(route_class=CommonRoute, prefix='/product', tags=['product'],
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

@product_router.get('', responses={200:{"model": Response[ListProductResponse]}})
@inject
def get_all(product_service: ProductService = Depends(Provide(Container.product_service))):
    """
        Get list product
    """
    data = product_service.get_all()
    payload = ListProductResponse(**data)
    response = ok(data=payload.dict())
    return response

@product_router.post('', tags=["product"], responses={200: {"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def add(request: ProductRequest,
        product_service: ProductService = Depends(Provide(Container.product_service))):
    """
        Add product
    """
    product_service.add(request.__dict__, context.user.value["username"])
    return ok()

# @product_router.get('/{product_id}', responses={200:{"model": Response[ProductResponse]}})
# @inject
# def get_by_product_id(product_id: int,
#         product_service: ProductService = Depends(Provide(Container.product_service))):
#     """
#         Get list product
#     """
#     data = product_service.get_by_product_id(product_id)
#     payload = ProductResponse(**data)
#     response = ok(data=payload.__dict__)
#     return response

# @product_router.put('/{product_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
# @permission([ROLE.ADMIN])
# @inject
# def update_product(product_id: int,
#         request: ProductRequest,
#         product_service: ProductService = Depends(Provide(Container.product_service))):
#     """
#         Update product
#     """
#     product_service.update(product_id, request.__dict__["name"], context.user.value["username"])
#     return ok()

# @product_router.delete('/{product_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
# @permission([ROLE.ADMIN])
# @inject
# def delete_product(product_id: int,
#         product_service: ProductService = Depends(Provide(Container.product_service))):
#     """
#         Delete product
#     """
#     product_service.delete(product_id, context.user.value["username"])
#     return ok()

# @product_router.put('/{product_id}/active', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
# @permission([ROLE.ADMIN])
# @inject
# def active_product(product_id: int,
#         product_service: ProductService = Depends(Provide(Container.product_service))):
#     """
#         Active product
#     """
#     product_service.active(product_id, context.user.value["username"])
#     return ok()
