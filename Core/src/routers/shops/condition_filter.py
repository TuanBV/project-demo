"""
  Condition filter router
"""

from fastapi import APIRouter, Depends
from containers import Container
from core import CrmException, ERR_MESSAGE
from dto.response import CRMResponse
from dto.request.shop import AddConditionFilterRequest
from dto.response.shop import AddConditionFilterResponse, ConditionFilterResponse, NumberOfCustomerResponse
from helpers.response import (ok)
from helpers import context
from helpers.kbn import USER_ROLE
from routers.common import SSVRoute
from dependencies import authorized_shop
from decorators import permission
from dependency_injector.wiring import inject, Provide
from crm_condition_filter import ConditionFilterService


router = APIRouter(
  route_class=SSVRoute,
)

# Add condition filter function
# Param:
#   @condition_filter: Add condition filter model
#   @shop_no: No. of shop
# Output:
#   return: HTTP response
@router.post("/condition-filter", tags=["shop"], responses={200: {"model": CRMResponse[AddConditionFilterResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def add(condition_filter: AddConditionFilterRequest, condition_filter_service: ConditionFilterService = Depends(Provide(Container.condition_filter_service))):
  # Get information shop from context
  shop = context.user.value
  # Set data condition
  filter_detail_data = {
    "exclusion_search": condition_filter.filter_detail.exclusion_search.dict(),
    "extended_search": condition_filter.filter_detail.extended_search.dict(),
    "search_key": condition_filter.filter_detail.search_key
  }
  condition_filter = {
    "filter_detail": filter_detail_data,
    "title": condition_filter.title
  }
  # Get id and shop_no of shop
  shop_account_id = shop["user"]["id"]
  shop_no = shop["user"]["shop_no"]

  # Add condition filter new
  payload = condition_filter_service.add(shop_no, condition_filter, shop_account_id)
  return ok(data=payload)


# Get condition filter function
# Param:
#   @db: database
# Output:
#   return: HTTP response
@router.get("/condition-filter", tags=["shop"], responses={200: {"model": CRMResponse[ConditionFilterResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def get_list_title(condition_filter_service: ConditionFilterService = Depends(Provide(Container.condition_filter_service))):
  # Get information shop from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Get list title condition filter
  result = condition_filter_service.get_list_title(shop_no)
  payload = ConditionFilterResponse(**result)
  return ok(data=payload.dict())


# Delete condition filter function
# Param:
#   @condition_filter_id: Id of item condition filter
# Output:
#   return: HTTP response
@router.delete("/condition-filter/{condition_filter_id}", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def delete(condition_filter_id: str, condition_filter_service: ConditionFilterService = Depends(Provide(Container.condition_filter_service))):
  # Get information shop from context
  shop = context.user.value
  # Check has condition_filter_id
  if not condition_filter_id:
    raise CrmException(message=ERR_MESSAGE.ERRMSG0022)

  # Get id and shop_no of shop
  shop_account_id = shop["user"]["id"]
  shop_no = shop["user"]["shop_no"]

  # Delete condition filter
  condition_filter_service.delete(shop_no, condition_filter_id, shop_account_id)
  return ok()


# Count number of customer function
# Param:
#   @shop_no: No. of shop
#   @condition_filter_id: Id of item condition filter
# Output:
#   return: HTTP response
@router.get("/condition-filter/{condition_filter_id}", tags=["shop"], responses={200: {"model": CRMResponse[NumberOfCustomerResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def count_customer(condition_filter_id: str, condition_filter_service: ConditionFilterService = Depends(Provide(Container.condition_filter_service))):
  # Get data shop from context
  shop = context.user.value
  shop_no = shop["user"]["shop_no"]

  # Check condition_filter_id
  if not condition_filter_id:
    raise CrmException(message=ERR_MESSAGE.ERRMSG0022)

  # Count customer of condition
  result = condition_filter_service.count_customer(shop_no, condition_filter_id)
  payload = NumberOfCustomerResponse(**result)

  return ok(data=payload.dict())
