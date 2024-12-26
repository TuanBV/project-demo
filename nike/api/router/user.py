from fastapi import APIRouter, Depends
from schema.user import UserRequest, UserResponse, LoginRequest, ListUserResponse
from user import UserService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import (ok, make_cookie)
from helpers.cookie import get_user_cookie
from dependencies import authorized_user
from router.common import CommonRoute
from helpers import context
from typing import List


user_router = APIRouter(route_class=CommonRoute, prefix='/user', tags=['user'],
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

@user_router.get('/me', responses={200:{"model": Response[UserResponse]}}, dependencies=[Depends(authorized_user)])
@inject
def get_me(user_service: UserService = Depends(Provide(Container.user_service))):
    """
        Get data user by cookie
    """
    # get data user
    data_user = user_service.get_me()
    # Set cookie
    cookie_config = make_cookie(get_user_cookie(), data_user["token"])
    payload = UserResponse(**data_user)
    response = ok(data=payload.dict())

    response.set_cookie(**cookie_config)

    return response

@user_router.post('/logout', dependencies=[Depends(authorized_user)])
@inject
def logout():
    context.user.reset()
    response = ok()
    cookie_config = make_cookie(get_user_cookie(), max_age=0)
    # Set cookie
    response.set_cookie(**cookie_config)
    return response

@user_router.post('/login', responses={200:{"model": Response[UserResponse]}})
@inject
def login(request: LoginRequest, user_service: UserService = Depends(Provide(Container.user_service))):
    """
        Login
    """
    # get data user
    data_user = user_service.login(request.__dict__)
    # Set cookie
    cookie_config = make_cookie(get_user_cookie(), data_user["token"])
    payload = UserResponse(**data_user["user"])
    response = ok(data=payload.dict())

    response.set_cookie(**cookie_config)

    return response


@user_router.post('', responses={200: {"model": Response[UserResponse]}})
@inject
def create(request: UserRequest, user_service: UserService = Depends(Provide(Container.user_service))):
    """
        Register a new user
    """
    data = user_service.create(request.dict())
    cookie_config = make_cookie(get_user_cookie(),data['token'])
    payload = UserResponse(**data)
    response = ok(data=payload.dict())

    # Set cookie
    response.set_cookie(**cookie_config)

    return response


@user_router.get('/all', responses={200:{"model": Response[ListUserResponse]}})
@inject
def get_list(user_service: UserService = Depends(Provide(Container.user_service))):
    """
        Get list user
    """
    # Get data user
    data_user = user_service.get_list()
    payload = ListUserResponse(**data_user)
    response = ok(data=payload.dict())

    return response


@user_router.post('/{user_id}/{status}', responses={200: {"model": Response[UserResponse]}})
@inject
def status_user(user_id: str, status: int, user_service: UserService = Depends(Provide(Container.user_service))):
    """
        Change status user
    """
    user_service.change_status(user_id, status)

    return ok()
