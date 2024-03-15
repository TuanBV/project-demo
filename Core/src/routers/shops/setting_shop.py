"""
Setting shop router
"""
from helpers.response import ok
from helpers import kbn
from helpers import context
from fastapi import APIRouter, Depends
from containers import Container
from dto.request.shop import RankShopRequest, SettingShopRequest, SettingShopCampaignRequest, SettingShopNotifyRequest
from dto.response import CRMResponse
from dto.response.shop import SettingShopNotifyResponse
from core import SUCCESS_MESSAGE
from routers.common import SSVRoute
from dependencies import authorized_shop
from decorators import permission
from crm_setting_shop import SettingShopService
from dependency_injector.wiring import inject, Provide





router = APIRouter(route_class=SSVRoute)

# Update shop account security function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@router.get("/customer/notify/{type_notify}", tags=["shop"], responses={200: {"model": CRMResponse[SettingShopNotifyResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.USER_ROLE.SHOP_OWNER, kbn.USER_ROLE.SHOP_MANAGER, kbn.USER_ROLE.SHOP_STAFF])
@inject
async def get_notify_shop(type_notify: int, setting_shop_service: SettingShopService = Depends(Provide(Container.setting_shop_service))):
  # Get information from shop
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]

  # Get notify of shop
  notify = setting_shop_service.get_notify_shop(shop_no, type_notify)
  payload = SettingShopNotifyResponse(**notify)

  # Don't notify
  if not notify:
    return ok(SUCCESS_MESSAGE.SUCMSG0021)
  return ok(data=payload.dict())


# Edit campaign shop function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@router.put("/campaign", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def edit_campaign(data_campaign: SettingShopCampaignRequest, setting_shop_service: SettingShopService = Depends(Provide(Container.setting_shop_service))):
  # Get information shop from context
  shop = context.user.value
  # Get shop_no
  shop_no = shop["user"]["shop_no"]

  # Get id of account shop
  shop_account_id = shop["user"]["id"]

  # Update campaign of shop
  setting_shop_service.update_campaign_shop(shop_no, data_campaign.dict(), shop_account_id)

  return ok()


# Edit notify shop function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@router.put("/customer/notify/{type_notify}", tags=["shop"],
    responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def edit_notify(type_notify: int, data: SettingShopNotifyRequest,
    setting_shop_service: SettingShopService = Depends(Provide(Container.setting_shop_service))):
  # Get information shop from context
  shop = context.user.value

  # Get shop_no
  shop_no = shop["user"]["shop_no"]

  # Get id of account shop
  shop_account_id = shop["user"]["id"]

  # Init data update
  content = data.dict()["content"]

  # Update notify of shop
  setting_shop_service.update_notify_shop(shop_no, content, type_notify, shop_account_id)

  return ok()


# Edit notify shop function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@router.put("/rank", tags=["shop"],
    responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def edit_rank(data: RankShopRequest,
    setting_shop_service: SettingShopService = Depends(Provide(Container.setting_shop_service))):
  # Get information shop from context
  shop = context.user.value
  # Get shop_no
  shop_no = shop["user"]["shop_no"]
  # Get id of account shop
  shop_account_id = shop["user"]["id"]

  # Init data update
  data_rank = data.dict()
  # Update rank of shop
  setting_shop_service.update_rank_shop(shop_no, data_rank, shop_account_id)

  return ok()


# Edit notify shop function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@router.put("/setting-shop", tags=["shop"],
    responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def edit_setting(data: SettingShopRequest,
    setting_shop_service: SettingShopService = Depends(Provide(Container.setting_shop_service))):
  # Get information shop from context
  shop = context.user.value
  # Get shop_no
  shop_no = shop["user"]["shop_no"]
  # Get id of account shop
  shop_account_id = shop["user"]["id"]
  # Init data update
  data_setting = data.dict()
  # Update setting of shop
  setting_shop_service.update_setting_shop(shop_no, data_setting, shop_account_id)

  return ok()

