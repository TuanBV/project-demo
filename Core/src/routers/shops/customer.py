
"""
Customer router
"""
from containers import Container
from helpers import context
from helpers import kbn
from helpers.response import ok
from fastapi import APIRouter, Depends
from dto.response import CRMResponse
from dto.response.shop import ActionByDateResponse, ListCustomerResponse, ExportCSVResponse, EditCustomerResponse
from dto.response.shop.manager_visit_store.get_customer import ActionByMonthResponse
from dto.request.shop import AddCustomerRequest, EmailRequest, EditCustomerRequest
from routers.common import SSVRoute
from dependencies import authorized_shop
from decorators import permission
from dependency_injector.wiring import inject, Provide

from crm_customer import CustomerService


router = APIRouter(route_class=SSVRoute)


# Get list customer
# Param:
#   @body: Data request
# Output:
#   return: JSONResponse
@router.get("/customer", tags=["shop"], responses={200: {"model": CRMResponse[ListCustomerResponse]}}, dependencies=[Depends(authorized_shop)])
@inject
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
async def get_list(search_key: str = "", extended_search: str = "", exclusion_search: str = "", limit: int = 20, offset: int = 1,
    sort_key: str = "", sort_type: str = "", query_path: str = "", act_detail_id: str = "", type_choose: str = "",
    customer_service: CustomerService = Depends(Provide(Container.customer_service))):
  # Get data shop from context
  shop = context.user.value
  # Init data
  query_params = {
    "search_key": search_key,
    "extended_search": extended_search,
    "exclusion_search": exclusion_search,
    "limit": limit,
    "offset": offset,
    "sort_key": sort_key,
    "sort_type": sort_type,
    "query_path": query_path,
    "act_detail_id": act_detail_id,
    "type_choose": type_choose
  }
  # Get shop_no from context
  shop_no = shop["user"]["shop_no"]
  # Get list customer
  result_list_customer = customer_service.get_list(query_params, shop_no, type_choose)
  payload = ListCustomerResponse(**result_list_customer)
  response = payload.dict()

  return ok(data=response)


# Add customer
# Param:
#   @shop_no: No. of shop
#   @mode: mode add customer
#   @data_customer: data customer model
# Output:
#   return: HTTP response
@router.post("/customer", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def add_customer(data_customer : AddCustomerRequest, customer_service: CustomerService = Depends(Provide(Container.customer_service))):
  # Get information from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Preparing data
  opt = {
    "data": data_customer.dict(),
    "me": context.user.value,
    "shop_no": shop_no,
  }
  # Add customer
  customer_service.add(opt)

  return ok()


# Edit customer
# Param:
#   @shop_no: No. of shop
#   @mode: mode add customer
#   @data_customer: data customer model
# Output:
#   return: HTTP response
@router.put("/customer/{customer_no}", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def edit_customer(customer_no: str, data_customer : EditCustomerRequest, customer_service: CustomerService=Depends(Provide(Container.customer_service))):
  # Get information from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Preparing data
  data = {
    "customers": data_customer.dict(),
    "me": shop,
    "shop_no": shop_no,
  }
  # Add customer
  customer_service.edit(data, customer_no)

  return ok()


# Check email
# Param:
#   @db: database
#   @data_customer: data customer model
# Output:
#   return: HTTP response
@router.post("/check-email", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def check_email_shop(data_request : EmailRequest, customer_service: CustomerService = Depends(Provide(Container.customer_service))):
  # Get information from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # check email exist
  customer_service.check_email_exist_in_shop(shop_no, data_request.dict())

  return ok()


# Export CSV
# Param:
#   @event: Data request
#   @customer_no: no of customer
# Output:
#   return: HTTP response
@router.get("/customer/csv", tags=["shop"], responses={200: {"model": CRMResponse[ExportCSVResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def export_csv(search_key: str = "", extended_search: str = "", exclusion_search: str = "", limit: int = 20, offset: int = 1,
    sort_key: str = "", sort_type: str = "", query_path: str = "", act_detail_id: str = "", type_choose: str = "",
    customer_service: CustomerService = Depends(Provide(Container.customer_service))):
  # Get information from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Init data
  query_params = {
    "search_key": search_key,
    "extended_search": extended_search,
    "exclusion_search": exclusion_search,
    "limit": limit,
    "offset": offset,
    "sort_key": sort_key,
    "sort_type": sort_type,
    "query_path": query_path,
    "act_detail_id": act_detail_id,
    "type_choose": type_choose
  }
  # Export CSV
  result = customer_service.export_csv(shop_no, query_params)
  payload = ExportCSVResponse(**result)

  return ok(data=payload.dict())


# Get customer by customer no
# Param:
#   @event: Data request
#   @customer_no: customer_no of customer
# Output:
#   return: HTTP response
@router.get("/customer/{customer_no}", tags=["shop"], responses={200: {"model": CRMResponse[EditCustomerResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def get_customer_by_customer_no(customer_no : str, customer_service: CustomerService = Depends(Provide(Container.customer_service))):
  # Get information from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Get customer by customer_no
  result = customer_service.get_by_customer_no(shop_no, customer_no)
  payload = EditCustomerResponse(**result)

  return ok(data=payload.dict())


# Get action by date
# Param:
#   @data: data
# Output:
#   return: HTTP response
@router.get("/customer/{customer_no}/action", tags=["shop"],
    responses={200: {"model": CRMResponse[ActionByDateResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def get_action_by_date(customer_no: str, start_date: str, end_date: str, month_filter: str, type_calendar: int,
    customer_service: CustomerService = Depends(Provide(Container.customer_service))):
  # Get information from context
  shop = context.user.value
  # Get shop_no
  shop_no = shop["user"]["shop_no"]
  # Get action of customer by date
  result = customer_service.get_action_customer_by_date(shop_no, customer_no, start_date, end_date, month_filter, type_calendar)
  payload = ActionByDateResponse(**result)

  return ok(data=payload.dict())


# Get action by date at get list customer
# Param:
#   @data_customer: data customer model
# Output:
#   return: HTTP response
@router.get("/customer/{customer_no}/action/month", tags=["shop"],
    responses={200: {"model": CRMResponse[ActionByMonthResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([kbn.UserRole.SHOP_OWNER, kbn.UserRole.SHOP_MANAGER, kbn.UserRole.SHOP_STAFF])
@inject
async def get_action_by_month(customer_no: str, month_filter: str, customer_service: CustomerService = Depends(Provide(Container.customer_service))):
  # Get information from context
  shop = context.user.value
  # Get shop_no
  shop_no = shop["user"]["shop_no"]
  # Get action of customer by month
  result = customer_service.get_action_by_month(shop_no, customer_no, month_filter)
  payload = ActionByMonthResponse(**{"item": result})

  return ok(data=payload.dict())
