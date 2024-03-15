"""
Manager visit store router
"""

from typing import Optional
from fastapi import APIRouter, Depends
from containers import Container
from crm_manager_visit_store import ManagerVisitStoreService
from dto.request.shop import NoteRequest, AddPointHistoriesRequest, EditPointHistoriesRequest
from dto.response import CRMResponse
from dto.response.shop import DashboardCustomerResponse
from helpers import kbn
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

# Get information customer by customer no
# Param:
#   @shop_no: No. of shop
#   @customer_no: No. of customer
#   @mode: mode get data customer
# Output:
#   return: HTTP response
@router.get("/customer/{customer_no}/information", tags=["shop"], responses={200: {"model": CRMResponse[DashboardCustomerResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def get_customer_by_customer_no(customer_no: str, mode: str, start_time: Optional[str] = None, type_calendar: Optional[int] = kbn.TYPE_CALENDAR.YEAR,
    manager_visit_store_service: ManagerVisitStoreService = Depends(Provide(Container.manager_visit_store_service))):
  # Get data from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Get info customer by customer no
  customer = manager_visit_store_service.get_customer_by_customer_no(shop_no, customer_no, mode, start_time, type_calendar)
  payload = DashboardCustomerResponse(**customer)

  return ok(data=payload.dict())


# Edit point histories
# Param:
#   @db: database
#   @customer_no: No. of customer
#   @point_id: id of point
# Output:
#   return: HTTP response
@router.put("/customer/{customer_no}/point/{point_id}", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def edit_point(customer_no: str, point_id: int, data: EditPointHistoriesRequest,
    manager_visit_store_service: ManagerVisitStoreService = Depends(Provide(Container.manager_visit_store_service))):
  # Get data from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  setting_rank = shop["user"]["shop"]["setting_rank"]
  # Edit point histories by id
  manager_visit_store_service.update_point(shop_no, customer_no, point_id, data.dict(), setting_rank, shop["user"]["id"])

  return ok()


# Add point histories
# Param:
#   @db: database
#   @customer_no: No. of customer
# Output:
#   return: HTTP response
@router.post("/customer/{customer_no}/point", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def add_point(customer_no: str, data: AddPointHistoriesRequest,
    manager_visit_store_service: ManagerVisitStoreService = Depends(Provide(Container.manager_visit_store_service))):
  # Get data from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  setting_rank = shop["user"]["shop"]["setting_rank"]
  # Add point histories
  manager_visit_store_service.add_point(shop_no, customer_no, data.dict(), setting_rank, shop["user"]["id"])

  return ok()


# Deleted point histories
# Param:
#   @db: database
#   @customer_no: No. of customer
#   @point_id: id of point
# Output:
#   return: HTTP response
@router.delete("/customer/{customer_no}/point/{point_id}", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def delete_point(customer_no: str, point_id,
    manager_visit_store_service: ManagerVisitStoreService = Depends(Provide(Container.manager_visit_store_service))):
  # Get data from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Get setting rank of shop
  setting_rank = shop["user"]["shop"]["setting_rank"]

  # # Delete point histories
  manager_visit_store_service.delete_point(shop_no, customer_no, point_id, setting_rank, shop["user"]["id"])

  return ok()


# Update note of customer
# Param:
#   @db: database
#   @data_customer: data customer model
# Output:
#   return: HTTP response
@router.put("/customer/{customer_no}/comment", tags=["shop"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([USER_ROLE.SHOP_OWNER, USER_ROLE.SHOP_MANAGER, USER_ROLE.SHOP_STAFF])
@inject
async def update_note_customer(customer_no: str, note_request : NoteRequest,
    manager_visit_store_service: ManagerVisitStoreService = Depends(Provide(Container.manager_visit_store_service))):
  # Get information from context
  shop = context.user.value
  # Get shop_no of shop
  shop_no = shop["user"]["shop_no"]
  # Update note of customer
  manager_visit_store_service.delete_note_customer(shop_no, customer_no, note_request.dict()["note"], shop["user"]["id"])

  return ok()
