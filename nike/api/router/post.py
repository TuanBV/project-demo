from fastapi import APIRouter, Depends
from schema.post import PostRequest, ListPostResponse, PostResponse
from post import PostService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import ok
from helpers import context
from dependencies import authorized_user
from router.common import CommonRoute
from utils.kbn import ROLE
from decorators import permission

post_router = APIRouter(route_class=CommonRoute, prefix='/post', tags=['post'],
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

@post_router.get('', responses={200:{"model": Response[ListPostResponse]}})
@inject
def get_all(post_service: PostService = Depends(Provide(Container.post_service))):
    """
        Get list post
    """
    data = post_service.get_all()
    payload = ListPostResponse(**data)
    response = ok(data=payload.dict())
    return response

@post_router.post('', tags=["post"], responses={200: {"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def add(request: PostRequest,
        post_service: PostService = Depends(Provide(Container.post_service))):
    """
        Add post
    """
    if request.id:
        post_service.update(request.id, request.__dict__, context.user.value["username"])
    else:
        post_service.add(request.__dict__, context.user.value["username"])
    return ok()

@post_router.get('/{post_id}', responses={200:{"model": Response[PostResponse]}})
@inject
def get_by_post_id(post_id: int,
        post_service: PostService = Depends(Provide(Container.post_service))):
    """
        Get list post
    """
    data = post_service.get_by_post_id(post_id)
    payload = PostResponse(**data)
    response = ok(data=payload.__dict__)
    return response

@post_router.delete('/{post_id}', responses={200:{"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def delete(post_id: int,
        post_service: PostService = Depends(Provide(Container.post_service))):
    """
        Delete post
    """
    post_service.delete(post_id, context.user.value["username"])
    return ok()
