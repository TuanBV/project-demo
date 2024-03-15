"""
Action router
"""

from containers import Container
from fastapi import APIRouter, Depends
from dto.response import CRMResponse
from dto.response.shop import ListActionsResponse, ListActionsChildResponse, GetActionResponse, GetActionDetailResponse, GetActionUpcomingResponse
from dto.request.shop import AddActionRequest, EditActionRequest
from crm_action import ActionService
from core import CrmException, ERR_MESSAGE
from routers.common import SSVRoute
from dependencies import authorized_shop
from helpers.response import (ok)
from helpers.kbn import UserRole
from helpers import context
from decorators import permission
from dependency_injector.wiring import inject, Provide


router = APIRouter(
  route_class=SSVRoute,
)

# Get list action shop no function
# Param:
#   @search_key: Text of user want to search
#   @limit: Limit item per page
#   @offset: Number of page
#   @sort_key: Column of user want to sort
#   @sort_type: Sort asc or desc
#   @action_status: Action status
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.get("/action", tags=["shop"], responses={200:{"model": CRMResponse[ListActionsResponse]}},dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def get_list(search_key: str = "", limit: int = 20, offset: int = 1, sort_key: str = "", sort_type: str = "",
    action_status: int = 0, action_service: ActionService = Depends(Provide[Container.action_service])):
  user = context.user.value

  # Set data for function in service
  data = {
    "shop_no": user["user"]["shop_no"],
    "search_key": search_key,
    "limit": limit,
    "offset": offset,
    "sort_key": sort_key,
    "sort_type": sort_type,
    "action_status": action_status
  }

  # Call function
  payload = action_service.get_list(data)
  payload = ListActionsResponse(**payload)
  response = ok(data=payload.dict())

  # Success
  return response


# Get action child in action details table function
# Param:
#   @action_code: Code of action
#   @offset: Offset
#   @limit: Limit
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.get("/action-child/{action_code}", tags=["shop"], responses={200:{"model": CRMResponse[ListActionsChildResponse]}},
  dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def get_list_child(action_code: str, offset: int, limit: int, action_service: ActionService = Depends(Provide[Container.action_service])):
  # Check action code not null
  if action_code == "":
    raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

  user = context.user.value

  # Set data for function in service
  data = {
    "shop_no": user["user"]["shop_no"],
    "action_code": action_code,
    "offset": offset,
    "limit": limit
  }

  # Call function
  payload = action_service.get_list_child(data)
  payload = ListActionsChildResponse(**payload)
  response = ok(data=payload.dict())

  # Success
  return response


# Delete action in action details table function
# Param:
#   @action_detail_id: Id action item in action details table
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.delete("/action-detail/{action_detail_id}", tags=["shop"], responses={200:{"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def delete_detail(action_detail_id: int, action_service: ActionService = Depends(Provide[Container.action_service])):
  user = context.user.value
  # Action detail id empty will return an error
  if not action_detail_id:
    raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

  # Set data for function in service
  data = {
    "shop_no": user["user"]["shop_no"],
    "action_detail_id": action_detail_id,
    "user": user["user"],
  }
  # Call function
  action_service.delete_detail(data)

  # Success
  return ok()


# Add action function
# Param:
#   @body: Data request
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.post("/action", tags=["shop"], responses={200:{"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def add(body: AddActionRequest, action_service: ActionService = Depends(Provide[Container.action_service])):
  user = context.user.value

  # Set data for function in service
  data = {
    "data_action": body.dict(),
    "user": user["user"],
    "shop_no": user["user"]["shop_no"]
  }

  # Call function
  action_service.add(data)

  # Success
  return ok()


# Get action in action table by action code function
# Param:
#   @action_code: Code of action
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.get("/action/{action_code}", tags=["shop"], responses={200:{"model": CRMResponse[GetActionResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def get(action_code: str, action_service: ActionService = Depends(Provide[Container.action_service])):
  user = context.user.value

  # Action code empty will raise error
  if action_code == "":
    raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

  # Set data for function in service
  data = {
    "shop_no": user["user"]["shop_no"],
    "action_code": action_code,
  }

  # Call function
  payload = action_service.get(data)
  payload = GetActionResponse(**payload)
  response = ok(data=payload.dict())

  # Success
  return response


# Delete all action not send by action id function
# Param:
#   @action_code: Code of action
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.delete("/action/{action_code}", tags=["shop"], responses={200:{"model": CRMResponse[GetActionResponse]}}, dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def delete(action_code: str, action_service: ActionService = Depends(Provide[Container.action_service])):
  user = context.user.value
  # Action code empty will raise error
  if action_code == "":
    raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

  data = {
    "shop_no": user["user"]["shop_no"],
    "action_code": action_code,
    "user": user["user"]
  }

  # Call function
  action_service.delete(data)

  # Success
  return ok()


# Get action in action detail table by id function
# Param:
#   @action_detail_id: Action detail id
#   @action_code: Code of action
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.get("/action-detail/{action_code}/{action_detail_id}", tags=["shop"], responses={200:{"model": CRMResponse[GetActionDetailResponse]}},
  dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def get_detail(action_code: str, action_detail_id: int, action_service: ActionService = Depends(Provide[Container.action_service])):
  user = context.user.value
  # Action detail id or action code empty will raise error
  if action_code is None or action_detail_id is None:
    raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

  # Set data for function in service
  data = {
    "shop_no": user["user"]["shop_no"],
    "action_detail_id": action_detail_id,
    "action_code": action_code
  }

  # Call function
  payload = action_service.get_detail(data)
  payload = GetActionDetailResponse(**payload)
  response = ok(data=payload.dict())

  # Success
  return response


# Edit action detail function
# Param:
#   @action_detail_id: Action detail id
#   @body: Data request
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.put("/action-detail/{action_detail_id}", tags=["shop"], responses={200:{"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def edit_detail(action_detail_id: int,body: EditActionRequest, action_service: ActionService = Depends(Provide[Container.action_service])):
  user = context.user.value
  # Action detail id empty will raise error
  if action_detail_id is None:
    raise CrmException(message = ERR_MESSAGE.ERRMSG0017)

  # Set data for function in service
  data = {
    "data_action": body.dict(),
    "user": user["user"],
    "shop_no": user["user"]["shop_no"],
    "action_detail_id": action_detail_id,
  }

  # Call function
  action_service.edit_detail(data)

  # Success
  return ok()


# Get action upcoming function
# Param:
#   @action_service: Action service
# Output:
#   return: HTTP response
@router.get("/action-upcoming", tags=["shop"], responses={200:{"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_shop)])
@permission([UserRole.SHOP_OWNER, UserRole.SHOP_MANAGER])
@inject
async def action_upcoming(action_service: ActionService = Depends(Provide[Container.action_service])):
  user = context.user.value

  # Call function
  payload = action_service.get_action_upcoming(user["user"]["shop_no"])

  payload = GetActionUpcomingResponse(**payload)
  response = ok(data=payload.dict())

  return response
