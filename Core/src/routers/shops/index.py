
"""
Shop router
"""

from typing import Optional
from fastapi import APIRouter, Depends, Header
from containers import Container
from dto.response import CRMResponse
from dto.request.shop import ShopLoginRequest, ResetPasswordRequest, AuthVerifyRequest, CheckTokenRequest, EmailVerificationRequest
from dto.response.shop import AllowOtpResponse, SendOtpResponse, CheckTokenResponse, ShopLoginResponse
from core import CrmException, CrmUnauthorizedException, ERR_MESSAGE
from helpers.const import (ONE_HOUR)
from helpers.cookie import get_shop_cookie, get_auth_cookie
from helpers.kbn import COOKIE_NAME
from helpers.response import (ok, make_cookie)
from helpers import context
from dependencies import authorized_shop, get_cookies_auth_two_step
from routers.common import SSVRoute
from routers.shops.customer import router as customer_routers
from routers.shops.shop_notify import router as shop_notify_routers
from routers.shops.shop_account import router as shop_account_routers
from routers.shops.customer_tag import router as customer_tags_routers
from routers.shops.condition_filter import router as condition_filter_routers
from routers.shops.manager_visit_store import router as manager_visit_store_routers
from routers.shops.action import router as action_routers
from routers.shops.template import router as template_routers
from routers.shops.setting_shop import router as setting_routers
from dependency_injector.wiring import inject, Provide
from crm_shop import ShopService


shop_routers = APIRouter(route_class=SSVRoute, tags=["shop"], prefix="/api/v1/shop",
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


shop_routers.include_router(customer_routers, tags=["shop"])
shop_routers.include_router(shop_notify_routers, tags=["shop"])
shop_routers.include_router(shop_account_routers, tags=["shop"])
shop_routers.include_router(customer_tags_routers, tags=["shop"])
shop_routers.include_router(condition_filter_routers, tags=["shop"])
shop_routers.include_router(manager_visit_store_routers, tags=["shop"])
shop_routers.include_router(action_routers, tags=["shop"])
shop_routers.include_router(template_routers, tags=["shop"])
shop_routers.include_router(setting_routers, tags=["shop"])


# Login to shop account
# Param:
#   @body: Data request
# Output:
#   return: JSONResponse
@shop_routers.post("/login", tags=["shop"], responses={200: {"model": CRMResponse[ShopLoginResponse]}})
@inject
async def login_shop(body: ShopLoginRequest, shop_service: ShopService = Depends(Provide(Container.shop_service))):
  # parse data json on body event
  opt = body.dict()
  result_login = shop_service.login(opt)
  # return payload
  # Turn on two-factor authentication
  if "two_fa_flg" in result_login:
    cookie_config = make_cookie(get_auth_cookie(), result_login["otp_token"], ONE_HOUR)
    response = ok(data={
      "two_fa_flg": int(result_login["two_fa_flg"]),
      "two_fa_kbn": int(result_login["two_fa_kbn"])
    })
  # Turn off two-factor authentication
  else:
    cookie_config = make_cookie(get_shop_cookie(), result_login["token"])
    payload = ShopLoginResponse(**result_login)
    response = ok(data=payload.dict())

  # Set cookie
  response.set_cookie(**cookie_config)

  return response


# Get login data of shop account
# Param:
#   None
# Output:
#   return: HTTP response
@shop_routers.get("/me", tags=["shop"], responses={200: {"model": CRMResponse[ShopLoginResponse]}}, dependencies=[Depends(authorized_shop)])
@inject
async def get_me(shop_service: ShopService = Depends(Provide(Container.shop_service))):
  # Get information of shop from context
  shop = context.user.value
  # Get shop_account_id from context
  shop_account_id = shop["user"]["id"]
  # remake token
  result_get_me = shop_service.get_user_me(shop_account_id)
  payload = ShopLoginResponse(**result_get_me)
  response = ok(data=payload.dict())

  cookie_config = make_cookie(get_shop_cookie(), payload.token)
  # Set cookie
  response.set_cookie(**cookie_config)

  return response


# Logout
# Param:
#  None
# Output:
#   return: HTTP response
@shop_routers.post("/logout", tags=["shop"], dependencies=[Depends(authorized_shop)])
async def logout():
  context.user.reset()
  response = ok()

  cookie_config = make_cookie(get_shop_cookie(), max_age=0)
  # Set cookie
  response.set_cookie(**cookie_config)

  return response


# Check token
# Param:
#   @shop_account_id: id account
#   @token: data token
# Output:
#   return: HTTP response
@shop_routers.post("/{shop_account_id}/token", tags=["shop"], responses={200: {"model": CRMResponse[CheckTokenResponse]}})
@inject
async def verify_token(shop_account_id: str, body: CheckTokenRequest, shop_service: ShopService = Depends(Provide(Container.shop_service))):
  data_check = {
    "token": body.token,
    "id": shop_account_id,
  }
  result_token = shop_service.verify_token(data_check)

  # Check token exist
  if result_token:
    data = {
        "email": result_token
    }
    payload = CheckTokenResponse(**data)
    return ok(data=payload.dict())

  # Token don't exist or end time token
  else:
    raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0042)


# Send mail forgot password
# Param:
#   @mail_address: mail of account
# Output:
#   return: HTTP response
@shop_routers.post("/email/verification", tags=["shop"], responses={200: {"model": CRMResponse[ShopLoginResponse]}})
@inject
async def mail_reset_password(body: EmailVerificationRequest, shop_service: ShopService = Depends(Provide(Container.shop_service))):
  mail_address = body.email
  shop_service.mail_reset_password(mail_address)

  return ok()


# Reset password
# Param:
#   @token: Token
#   @shop_account_id: Id account
#   @reset_password: ResetPassword model
# Output:
#   return: HTTP response
@shop_routers.patch("/{shop_account_id}/password", tags=["shop"], responses= {200: {"model": CRMResponse[dict]}})
@inject
async def reset_password(shop_account_id: str, reset_pw: ResetPasswordRequest,
    token: Optional[str] = Header(default=None), shop_service: ShopService = Depends(Provide(Container.shop_service))):
  # Check data token
  if token:
    data_check = {
        "token": token,
        "id": shop_account_id,
    }
    result_token = shop_service.verify_token(data_check)
    # Reset password if token valid
    if result_token:
      data_password = {
        "password_new": reset_pw.password_new,
        "confirm_password": reset_pw.confirm_password
      }

      opt = {
        "password" : data_password,
        "token": token,
        "id": shop_account_id,
        "updated_user": "system",
      }
      payload = shop_service.reset_password(opt)
      # Update password success
      if payload:
        return ok(data=[])

      raise CrmException(message=ERR_MESSAGE.ERRMSG0040)
  raise CrmException(message=ERR_MESSAGE.ERRMSG0042)


# Verify OTP
# Param:
#   @opt: Otp code
#   @time_now: Current time
#   @time_remaining: Time expiried
# Output:
#   return: HTTP response
@shop_routers.post("/auth2/verify", tags=["shop"], responses={200: {"model": CRMResponse[ShopLoginResponse]}})
@inject
async def auth_two_step(body: AuthVerifyRequest, cookies: str = Depends(get_cookies_auth_two_step), shop_service: ShopService = Depends(Provide(Container.shop_service))):
  # Init data
  opt = {
    "otp": body.otp,
    "time_now": body.time_now,
    "time_remaining": body.time_remaining,
  }
  # Have a cookie
  if cookies:
    result_login = shop_service.auth_two_step(opt, cookies)

  # Don't have a cookie
  else:
    raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0180)

  # Success
  cookie_config = make_cookie(get_shop_cookie(), result_login["token"])
  payload = ShopLoginResponse(**result_login)
  response = ok(data=payload.dict())
  # Delete cookie
  response.delete_cookie(key=COOKIE_NAME.TOKEN_TWO_AUTHEN)
  # Set cookie
  response.set_cookie(**cookie_config)
  return response


# Send OTP
# Param:
#   None
# Output:
#   return: HTTP response
@shop_routers.get("/otp/send", tags=["shop"], responses={200: {"model": CRMResponse[SendOtpResponse]}})
@inject
async def send_otp(cookies: str = Depends(get_cookies_auth_two_step), shop_service: ShopService = Depends(Provide(Container.shop_service))):
  payload = {}
  # Have a cookie
  if cookies:
    payload = shop_service.send_otp(cookies)
    response = ok(data=payload)

  # Don't have a cookie
  else:
    raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0180)

  cookie_config = make_cookie(get_auth_cookie(), payload["otp_token"], ONE_HOUR)
  # Set cookie
  response.set_cookie(**cookie_config)

  return response


# Check token auth 2 step
# Param:
#   None
# Output:
#   return: HTTP response
@shop_routers.get("/auth2/token", tags=["shop"], responses={200: {"model": CRMResponse[AllowOtpResponse]}})
@inject
async def check_allow_otp_confirm(cookies: str = Depends(get_cookies_auth_two_step), shop_service: ShopService = Depends(Provide(Container.shop_service))):
  payload = {}
  # Have a cookie
  if cookies:
    payload = shop_service.check_allow_otp_confirm(cookies)

  # Don't have a cookie
  else:
    raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0180)

  return ok(data=payload)
