
"""
Shop router
"""

from fastapi import APIRouter, Depends
from containers import Container
from dto.response import Response
from dto.request.shop import ShopLoginRequest
from dto.response.shop import ShopLoginResponse
from helpers.cookie import get_shop_cookie
from helpers.response import (ok, make_cookie)
from helpers import context
from dependencies import authorized_shop
from dependency_injector.wiring import inject, Provide
from shop import ShopService
from routers.common import SSVRoute

shop_routers = APIRouter(route_class=SSVRoute, tags=["FastApi"], prefix="/api/v1/shop",
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

# Login to shop account
# Param:
#   @body: Data request
# Output:
#   return: JSONResponse
@shop_routers.post("/login", tags=["FastApi"], responses={200: {"model": Response[ShopLoginResponse]}})
@inject
async def login_shop(body: ShopLoginRequest, shop_service: ShopService = Depends(Provide(Container.shop_service))):
  # parse data json on body event
  opt = body.dict()
  result_login = shop_service.login(opt)

  cookie_config = make_cookie(get_shop_cookie(), result_login["token"])
  payload = ShopLoginResponse(**result_login["shop"])
  response = ok(data=payload.dict())

  # Set cookie
  response.set_cookie(**cookie_config)

  return response


# Logout
# Output:
#   return: HTTP response
@shop_routers.post("/logout", tags=["FastApi"], dependencies=[Depends(authorized_shop)])
async def logout():
  context.user.reset()
  response = ok()

  cookie_config = make_cookie(get_shop_cookie(), max_age=0)
  # Set cookie
  response.set_cookie(**cookie_config)

  return response
