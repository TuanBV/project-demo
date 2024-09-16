"""
Service owner router
"""
from fastapi import APIRouter, Depends
from containers import Container
from decorators import permission
# from dto.request.admin import AdminLoginRequest, AddShopRequest, EditShopRequest, EditShopNotifyRequest
from dto.response.admin import AdminLoginResponse, ListShopResponse, GetShopResponse, ExportShopCsvResponse, ShopNotifyResponse
from dto.response import CRMResponse
from core import CommonException, ERR_MESSAGE, SUCCESS_MESSAGE
# from crm_service_owner.services import ServiceOwner
from helpers.cookie import get_admin_cookie
from helpers.kbn import UserRole
from helpers import context
from helpers.response import (ok, make_cookie)
from routers.common import SSVRoute
from routers.admins.print import print_routers
from dependencies import authorized_admin
from dependency_injector.wiring import inject, Provide



admin_routers = APIRouter(
    route_class=SSVRoute,
    tags=["service_owner"],
    prefix="/api/v1/admin",
    responses={
      200: {
        "model": CRMResponse
      },
      401: {
        "model": CRMResponse[dict]
      },
      404: {
        "description": "No data",
        "model": CRMResponse[dict]
      },
      400: {
        "description": "API ERROR",
        "model": CRMResponse[dict]
      },
      500: {
        "description": "SYSTEM ERROR",
        "model": CRMResponse[dict]
      },
    },
  )

admin_routers.include_router(print_routers, tags=["service_owner"])


# # Admin login function
# # Param:
# #   @body: Data request
# #   @owner_service: Onwer service
# # Output:
# #   return: HTTP response
# @admin_routers.post("/login", tags=["service_owner"], responses={200:{"model": CRMResponse[AdminLoginResponse]}})
# @inject
# async def login(body: AdminLoginRequest, owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   payload = owner_service.admin_login(body.dict())
#   token = payload["token"]
#   del payload["token"]
#   payload = AdminLoginResponse(**payload)
#   response = ok(data=payload.dict())

#   cookie_config = make_cookie(get_admin_cookie(), token)
#   response.set_cookie(**cookie_config)
#   return response


# # Check data admin function
# # Param:
# #   @owner_service: Owner service
# # Output:
# #   return: HTTP response
# @admin_routers.get("/me", tags=["service_owner"], responses={200:{"model": CRMResponse[AdminLoginResponse]}}, dependencies=[Depends(authorized_admin)])
# @inject
# def get_me(owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   user = context.user.value
#   # remake token
#   payload = owner_service.get_admin_me(user["user"]["id"])
#   token = payload["token"]
#   del payload["token"]
#   payload = AdminLoginResponse(**payload)
#   response = ok(data=payload.dict())

#   cookie_config = make_cookie(get_admin_cookie(), token)
#   response.set_cookie(**cookie_config)
#   return response


# # Logout
# # Param: None
# # Output:
# #   return: HTTP response
# @admin_routers.post("/logout", tags=["service_owner"], dependencies=[Depends(authorized_admin)])
# @inject
# async def logout():
#   context.user.reset()
#   response = ok()

#   cookie_config = make_cookie(get_admin_cookie(), max_age=0)
#   response.set_cookie(**cookie_config)
#   return response


# # Get list shop function
# # Param:
# #   @search_key: Text of user want to search
# #   @limit: Limit item per page
# #   @offset: Number of page
# #   @sort_key: Column of user want to sort
# #   @sort_type: Sort asc or desc
# #   @exteded_seach: Search condition
# #   @owner_service: Owner service
# # Output:
# #   return: HTTP response
# @admin_routers.get("/shop", tags=["service_owner"], responses={200: {"model": CRMResponse[ListShopResponse]}}, dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def get_list_shop(search_key: str = "", limit: int = 20, offset: int = 1, sort_key: str = "", sort_type: str = "", extended_search: str = "",
#     owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   query_params = {
#     "search_key": search_key,
#     "extended_search": extended_search,
#     "limit": limit,
#     "offset": offset,
#     "sort_key": sort_key,
#     "sort_type": sort_type,
#   }
#   payload = owner_service.get_list_shop(query_params)
#   payload = ListShopResponse(**payload)
#   response = ok(data=payload.dict())

#   return response


# # Add shop function
# # Param:
# #   @body: Data request
# #   @owner_service: Owner service
# # Output:
# #   return: HTTP response
# @admin_routers.post("/shop", tags=["service_owner"], responses={200:{"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def add_shop(body: AddShopRequest, owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   user = context.user.value

#   data = {
#     "shop": body.shop.dict(),
#     "owner_account":  body.owner.dict(),
#     "user": user["user"]["id"]
#   }

#   # Check data account exist
#   if body.manager:
#     data["manager_account"] = body.manager.dict()

#   if body.staff:
#     data["staff_account"] = body.staff.dict()

#   owner_service.add_shop(data)
#   return ok()


# # Export csv in list shop function
# # Param:
# #   @search_key: Text of user want to search
# #   @limit: Limit item per page
# #   @offset: Number of page
# #   @sort_key: Column of user want to sort
# #   @sort_type: Sort asc or desc
# #   @exteded_seach: Search condition
# #   @owner_service: Owner service
# # Output:
# #   return: HTTP response
# @admin_routers.get("/shop/csv", tags=["service_owner"], responses={200:{"model": CRMResponse[ExportShopCsvResponse]}}, dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def export_csv(search_key: str = "", limit: int = 20, offset: int = 1, sort_key: str = "", sort_type: str = "", extended_search: str = "",
#     owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   query_params = {
#     "search_key": search_key,
#     "extended_search": extended_search,
#     "limit": limit,
#     "offset": offset,
#     "sort_key": sort_key,
#     "sort_type": sort_type,
#   }

#   payload = owner_service.export_csv(query_params)

#   return ok(data=payload)


# # Get shop function
# # Param:
# #   @shop_no: Shop no from path
# #   @owner_service: Owner service
# # Output:
# #   return: HTTP response
# @admin_routers.get("/shop/{shop_no}",tags=["service_owner"],responses={200: { "model": CRMResponse[GetShopResponse] }},dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def get_shop(shop_no: str, owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   # shop_no is empty will return an error
#   if shop_no == "":
#     raise CrmException(message = ERR_MESSAGE.ERRMSG0053)

#   payload = owner_service.get_shop(shop_no)
#   payload = GetShopResponse(**payload)
#   response = ok(SUCCESS_MESSAGE.SUCMSG0002, data=payload.dict())

#   return response


# # Edit shop function
# # Param:
# #   @shop_no: Shop no from path
# #   @body: Data request
# #   @owner_service: Owner service
# # Output:
# #   return: HTTP response
# @admin_routers.put("/shop/{shop_no}", tags=["service_owner"],responses={200: {"model": CRMResponse[dict]}},dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def edit_shop(shop_no: str, body: EditShopRequest, owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   # If shop_no empty will return an error
#   if shop_no == "":
#     raise CrmException(message = ERR_MESSAGE.ERRMSG0178)

#   user = context.user.value
#   data = {
#     "shop": body.shop.dict(),
#     "owner_account":  body.owner.dict(),
#     "user": user["user"]["id"],
#     "shop_no": shop_no
#   }
#   # Check data account exist
#   if body.manager:
#     data["manager_account"] = body.manager.dict()

#   if body.staff:
#     data["staff_account"] = body.staff.dict()

#   owner_service.edit_shop(data)

#   return ok()


# # Get shop notify function
# # Param:
# #   @owner_service: Owner service
# # Output:
# #   return: HTTP response
# @admin_routers.get("/setting/notify", tags=["service_owner"],responses={200: {"model": CRMResponse[ShopNotifyResponse]}},dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def get_shop_notify(owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   payload = owner_service.get_shop_notify()

#   payload = ShopNotifyResponse(**payload)

#   response = ok(SUCCESS_MESSAGE.SUCMSG0016, data=payload.dict())

#   return response


# # Edit shop notify function
# # Param:
# #   @body: Data request
# #   @owner_service: Owner service
# # Output:
# #   return: HTTP response
# @admin_routers.put("/setting/notify", tags=["service_owner"],responses={200: {"model": CRMResponse[dict]}},dependencies=[Depends(authorized_admin)])
# @permission([UserRole.ADMIN])
# @inject
# async def edit_shop_notify(body: EditShopNotifyRequest, owner_service: ServiceOwner = Depends(Provide[Container.services_owner])):
#   user = context.user.value

#   data = {
#     "notify_content": body.content,
#     "user": user["user"]["id"]
#   }

#   owner_service.edit_shop_notify(data)

#   return ok()
