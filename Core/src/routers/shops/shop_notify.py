"""
Shop notify router
"""
from helpers import context
from helpers.response import (ok)
from helpers.kbn import USER_ROLE, OpenStatus
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends
from containers import Container
from dto.response import CRMResponse
from dto.response.shop import CheckNotifyResponse, NotifyResponse
from core import CrmNoDataException, ERR_MESSAGE
from routers.common import SSVRoute
from dependencies import authorized_shop
from decorators import permission
from dependency_injector.wiring import inject, Provide
from crm_shop_notify import ShopNotifyService

router = APIRouter(route_class=SSVRoute)

# Get shop notify by shop no function
# Param:
#   @shop_account_id: Id of shop account
# Output:
#   return: HTTP response
@router.get("/notify", tags=["shop"], responses={200: {"model": CRMResponse[CheckNotifyResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def get_shop_notify(shop_notify_service: ShopNotifyService = Depends(Provide(Container.shop_notify_service))):
  # Get information shop from context
  shop = context.user.value["user"]
  notify = jsonable_encoder(shop_notify_service.get_shop_notify_by_shop_account_id(shop.get("id")))
  # Check notify
  if notify:
    payload = CheckNotifyResponse(**notify)
    response = payload.dict()
    return ok(data=response)
  else:
    raise CrmNoDataException(message=ERR_MESSAGE.ERRMSG0175)


# Update read flag of notify
# Output:
#   return: HTTP response
@router.put("/notify", tags=["shop"], responses={200: {"model": CRMResponse[NotifyResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def update_status(shop_notify_service: ShopNotifyService = Depends(Provide(Container.shop_notify_service))):
  # Get information shop from context
  shop = context.user.value["user"]
  notify_status = shop_notify_service.get_shop_notify_by_shop_account_id(shop.get("id"))
  # Check status of notify
  if notify_status:
    # Check read_flg
    if notify_status.read_flg.value == OpenStatus.OFF.value:
      # Update read_flag of notify
      shop_notify_service.update_status(shop.get("id"), notify_status.shop_notification_id)
    payload = NotifyResponse(**notify_status)
    response = payload.dict()
    return ok(data=response)
  else:
    raise CrmNoDataException(message=ERR_MESSAGE.ERRMSG0175)
