"""
Shop account router
"""

from fastapi import APIRouter, Depends
from containers import Container
from crm_shop.services import ShopService
from dto.response import CRMResponse
from dto.request.shop import SecurityRequest
from dto.response.shop import SecurityResponse
from helpers.response import (ok)
from helpers.kbn import USER_ROLE
from helpers import context
from routers.common import SSVRoute
from dependencies import authorized_shop
from decorators import permission
from dependency_injector.wiring import inject, Provide


router = APIRouter(
  route_class=SSVRoute,
)

# Update shop account security function
# Param:
#   @security: SecurityRequest Model,
# Output:
#   return: HTTP response
@router.put("/security", tags=["shop"], responses={200: {"model": CRMResponse[SecurityResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def update_security(security: SecurityRequest, shop_service: ShopService = Depends(Provide(Container.shop_service))):
  # Get information from context
  shop = context.user.value["user"]
  # Get shop_no of shop
  shop_no = shop["shop_no"]
  # Get id of account shop
  shop_account_id = shop["id"]
  # Init data update
  data = security.dict()

  # Update security
  result = shop_service.update_security(shop_no, data, shop_account_id)
  payload = SecurityResponse(**result)
  return ok(data=payload.dict())
