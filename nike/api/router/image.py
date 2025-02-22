from fastapi import APIRouter, Depends
from schema.image import ImageRequest, ListImageResponse
from image import ImageService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import ok
from helpers import context
from dependencies import authorized_user
from router.common import CommonRoute
from utils.kbn import ROLE
from decorators import permission

image_router = APIRouter(route_class=CommonRoute, prefix='/image', tags=['image'],
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

@image_router.get('', tags=["image"], responses={200:{"model": Response[ListImageResponse]}}, dependencies=[Depends(authorized_user)])
@inject
def get_all(image_service: ImageService = Depends(Provide(Container.image_service))):
    """
        Get list image
    """
    data = image_service.get_all()
    payload = ListImageResponse(**data)
    response = ok(data=payload.dict())
    return response


@image_router.post('', tags=["image"], responses={200: {"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def add(request: ImageRequest,
        image_service: ImageService = Depends(Provide(Container.image_service))):
    """
        Add image
    """
    image_service.add(request.__dict__, context.user.value["username"])
    return ok()

@image_router.delete('/{image_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def delete_image(image_id: int,
        image_service: ImageService = Depends(Provide(Container.image_service))):
    """
        Delete image
    """
    image_service.delete(image_id, context.user.value["username"])
    return ok()
