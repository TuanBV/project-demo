from fastapi import APIRouter, Depends
from schema.setting import SettingRequest, ListSettingResponse, SettingResponse
from setting import SettingService
from dependency_injector.wiring import inject, Provide
from containers import Container
from dto.response import Response
from helpers.response import ok
from helpers import context
from dependencies import authorized_user
from router.common import CommonRoute
from utils.kbn import ROLE
from decorators import permission

setting_router = APIRouter(route_class=CommonRoute, prefix='/setting', tags=['setting'],
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

@setting_router.get('/all', tags=["setting"], responses={200:{"model": Response[ListSettingResponse]}}, dependencies=[Depends(authorized_user)])
@inject
def get_all(setting_service: SettingService = Depends(Provide(Container.setting_service))):
    """
        Get list setting
    """
    data = setting_service.get_all()
    payload = ListSettingResponse(**data)
    response = ok(data=payload.dict())
    return response

@setting_router.get('', tags=["setting"], responses={200:{"model": Response[SettingResponse]}}, dependencies=[Depends(authorized_user)])
@inject
def get_new_setting(setting_service: SettingService = Depends(Provide(Container.setting_service))):
    """
        Get new setting
    """
    data = setting_service.get_new_setting()
    if data:
        payload = SettingResponse(**data)
        response = ok(data=payload.dict())
        return response


@setting_router.post('', tags=["setting"], responses={200: {"model": Response}}, dependencies=[Depends(authorized_user)])
@permission([ROLE.ADMIN])
@inject
def save(request: SettingRequest,
        setting_service: SettingService = Depends(Provide(Container.setting_service))):
    """
        Save info about setting
    """
    setting_service.save(request.__dict__, context.user.value["username"])
    return ok()
