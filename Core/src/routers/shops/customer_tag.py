"""
  Customer tags router
"""
from fastapi import APIRouter, Depends
from containers import Container
from dto.response import CRMResponse
from dto.response.shop import AddCustomerTagsResponse, CustomerTagsResponse
from dto.request.shop import CustomerTagsRequest
from helpers.response import (ok)
from helpers import context
from helpers.kbn import USER_ROLE
from routers.common import SSVRoute
from dependencies import authorized_shop
from decorators import permission
from dependency_injector.wiring import inject, Provide
from crm_customer_tags import CustomerTagsService



router = APIRouter(route_class=SSVRoute)

# Add customer tags function
# Param:
#   @shop_no: shop_no of shop
# Output:
#   return: HTTP response
@router.post("/customer-tags", tags=["shop"], responses={200: {"model":CRMResponse[AddCustomerTagsResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def add(customer_tag: CustomerTagsRequest,
    customer_tags_service: CustomerTagsService = Depends(Provide(Container.customer_tags_service))):
  # Get information shop from context
  shop = context.user.value
  body = {
    "title": customer_tag.title,
    "list_customer_no": customer_tag.list_customer_no
  }

  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]

  # Init data
  data = body # data request
  shop_account_id = shop["user"]["id"]

  # Add customer tags new
  payload = customer_tags_service.add(shop_no, data, shop_account_id)

  return ok(data=payload)


# Get customer tags function
# Param:
#   @shop_no: No. of shop
# Output:
#   return: HTTP response
@router.get("/customer-tags", tags=["shop"], responses={200: {"model": CRMResponse[CustomerTagsResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def get_list_title(customer_tags_service: CustomerTagsService = Depends(Provide(Container.customer_tags_service))):
  # Get information shop from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Get list customer tags
  result = customer_tags_service.get_list_title(shop_no)
  payload = CustomerTagsResponse(**result)

  return ok(data=payload.dict())


# Delete customer tags function
# Param:
#   @shop_no: No. of shop
#   @customer_tag_id: Id of item customer tags
# Output:
#   return: HTTP response
@router.delete("/customer-tags/{customer_tag_id}", tags=["shop"], responses={200: {"model": CRMResponse[CustomerTagsResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def delete(customer_tag_id: str,
    customer_tags_service: CustomerTagsService = Depends(Provide(Container.customer_tags_service))):
  # Get information from context
  shop = context.user.value

  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]

  # Get shop_account_id
  shop_account_id = shop["user"]["id"]

  # Delete customer tags
  customer_tags_service.delete(shop_no, customer_tag_id, shop_account_id)

  return ok()


# Add customer tags in list function
# Param:
#   @shop_no: No. of shop
#   @customer_tag_id: Id of item customer tags
#   @customer_id: Id of customer
# Output:
#   return: HTTP response
@router.post("/customer-tags/{customer_no}/{customer_tag_id}", tags=["shop"],
    responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def add_customer_in_list(customer_no: str, customer_tag_id: str, customer_tags_service: CustomerTagsService = Depends(Provide(Container.customer_tags_service))):
  # Get information from context
  shop = context.user.value

  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  shop_account_id = shop["user"]["id"]

  # Add customer in list
  customer_tags_service.add_customer_in_list(shop_no, customer_no, customer_tag_id, shop_account_id)

  return ok()


# Delete customer tags function
# Param:
#   @shop_no: No. of shop
#   @customer_tag_id: Id of item customer tags
#   @customer_id: Id of customer
# Output:
#   return: HTTP response
@router.delete("/customer-tags/{customer_no}/{customer_tag_id}", tags=["shop"],
    responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def delete_customer_in_list(customer_no: str, customer_tag_id: int,
    customer_tags_service: CustomerTagsService = Depends(Provide(Container.customer_tags_service))):
  # Get information from context
  shop = context.user.value

  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  shop_account_id = shop["user"]["id"]

  # Delete customer in lis
  customer_tags_service.delete_customer_in_list(shop_no, customer_no, customer_tag_id, shop_account_id)

  return ok()
