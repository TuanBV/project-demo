""" Member Controller """

from helpers import context
from helpers.const import CODE
from helpers.cookie import get_member_cookie
from helpers.response import (ok, make_cookie, ng)
from containers import Container
from crm_member.services import MemberService
from fastapi import APIRouter, Header, Depends
from dto.request.member import (MemberChangePasswordRequest, MemberLoginRequest, MemberSignUpTempRequest, MemberSendMailRequest, MemberEditRequest, MemberRegisterRequest, CheckUrlRequest)
from dto.response.member import (MemberNotifyResponse, CheckUrlResponse, MemberLoginResponse, MemberCheckNotifyResponse, MemberEditResponse, MemberTokenResponse, MemberRegisterResponse)
from dto.response import CRMResponse
from core import SUCCESS_MESSAGE
from routers.common import SSVRoute
from dependencies import authorized_member
from dependency_injector.wiring import inject, Provide


member_routers = APIRouter(
  route_class=SSVRoute,
  tags=["member"],
  prefix="/api/v1/member",
  responses={
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

# Check URL in member page function
# Param:
#  @data: data request
# Output:
#  return: data shop
@member_routers.post("/url", tags=["member"], responses={200: {"model": CRMResponse[CheckUrlResponse]}})
@inject
async def check_url(body: CheckUrlRequest, member_service: MemberService = Depends(Provide[Container.member_service])):
  # Check url and get data shop
  data_shop = member_service.check_url(body)
  payload = CheckUrlResponse(**data_shop)

  return ok(data=payload.dict())


# Login to member account
# Param:
#   @body: Data request
# Output:
#   return: HTTP response
@member_routers.post("/{shop_no}/login", tags=["member"], responses={200: {"model": CRMResponse[MemberLoginResponse]}})
@inject
async def login(shop_no: str, body: MemberLoginRequest, member_service: MemberService = Depends(Provide[Container.member_service])):
  data_member = member_service.login(body, shop_no)
  payload = MemberLoginResponse(**data_member)
  response = ok(SUCCESS_MESSAGE.SUCMSG0010, data=payload.dict())

  cookie_config = make_cookie(get_member_cookie(), payload.token)
  response.set_cookie(**cookie_config)
  return response


# Member change password function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.patch("/{shop_no}/{customer_id}/password", tags=["member"], responses={200: {"model": CRMResponse[dict]}})
@inject
async def change_password(shop_no: str, customer_id: str, body: MemberChangePasswordRequest, token: str = Header(default=None),
                          member_service: MemberService = Depends(Provide[Container.member_service])):
  opt = body.dict()
  opt["shop_no"] = shop_no
  opt["customer_id"] = customer_id
  opt["token"] = token
  # When have Token in headers
  # Call function check token
  ressult_token = ""
  if token:
    data_check = {
      "token": token,
      "customer_id": customer_id,
      "shop_no": shop_no,
    }
    ressult_token = member_service.verify_token(data_check)

  # Check token success
  if ressult_token:
    # Check token success
    member_service.change_password(opt)
    response = ok(SUCCESS_MESSAGE.SUCMSG0010)
  else:
    response = ng(code=CODE.API.INVALID_TOKEN)

  return response


# Check token function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.post("/{shop_no}/{customer_id}/token", tags=["member"], responses={200: {"model": CRMResponse[MemberTokenResponse]}})
@inject
def check_token(shop_no: str, customer_id: str, token: str = Header(default=None),
                      member_service: MemberService = Depends(Provide[Container.member_service])):
  opt = {
    "token" : token,
    "shop_no" : shop_no,
    "customer_id" : customer_id
  }

  member_email = member_service.verify_token(opt)
  # Have data customer
  if member_email:
    payload = MemberTokenResponse(email=member_email)
    return ok(SUCCESS_MESSAGE.SUCMSG0006, payload.dict())
  # Don't have data customer
  else:
    return ng(code=CODE.API.INVALID_TOKEN)


# Sign up temporary customer function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.post("/{shop_no}/temp", tags=["member"], responses={200: {"model": CRMResponse}})
@inject
async def sign_up_temp(shop_no: str, body: MemberSignUpTempRequest, member_service: MemberService = Depends(Provide[Container.member_service])):
  data = body.dict()
  data["shop_no"] = shop_no
  member_service.sign_up_temporary(data)
  return ok(SUCCESS_MESSAGE.SUCMSG0009)


# Member register function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.put("/{shop_no}/register", tags=["member"], responses={200: {"model": CRMResponse[MemberRegisterResponse]}})
@inject
async def register(shop_no: str, body: MemberRegisterRequest, token: str = Header(default=None),
                          member_service: MemberService = Depends(Provide[Container.member_service])):
  opt = body.dict()
  data = {
    "data": opt,
    "shop_no": shop_no,
  }
  # Call function check token
  ressult_token = ""
  if token:
    data_check = {
      "token": token,
      "customer_id": body.customer_tmp_id,
      "shop_no": shop_no,
    }
    ressult_token = member_service.verify_token(data_check)

  # Check token success
  if ressult_token != "":
    data_member = member_service.register(data)
    payload = MemberRegisterResponse(**data_member)
    response = ok(SUCCESS_MESSAGE.SUCMSG0010, data=payload.dict())

    cookie_config = make_cookie(get_member_cookie(), payload.token)
    response.set_cookie(**cookie_config)

    return response
  else:
    return ng(code=CODE.API.INVALID_TOKEN)


# Change status notify function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.put("/notify/{notify_kbn}", tags=["member"], responses={200: {"model": CRMResponse[MemberNotifyResponse]}}, dependencies=[Depends(authorized_member)])
@inject
async def open_notify(notify_kbn: int, member_service: MemberService = Depends(Provide[Container.member_service])):
  user = context.user.value

  result = member_service.open_notify(notify_kbn, user["user"])

  payload = MemberNotifyResponse(**result)

  response = ok(data=payload.dict())

  return response


# Member edit function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.put("", tags=["member"], responses={200: {"model": CRMResponse[MemberEditResponse]}}, dependencies=[Depends(authorized_member)])
@inject
async def edit(body: MemberEditRequest, member_service: MemberService = Depends(Provide[Container.member_service])):
  # Get information from context
  user = context.user.value["user"]
  data_member = body.dict()

  # Get shop_no, customer_no
  shop_no = user["shop_no"]
  customer_no = user["customer_no"]
  customer_id = user["id"]
  email = user["email"]

  result_member = member_service.edit(shop_no, customer_no, email, data_member, customer_id)
  payload = MemberEditResponse(**result_member)
  response = ok(data=payload.dict())

  cookie_config = make_cookie(get_member_cookie(), payload.token)
  response.set_cookie(**cookie_config)

  return response


  # Member edit function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.delete("", tags=["member"], responses={200: {"model": CRMResponse[dict]}}, dependencies=[Depends(authorized_member)])
@inject
async def delete(member_service: MemberService = Depends(Provide[Container.member_service])):
  # Get information from context
  user = context.user.value["user"]

  shop_no = user["shop_no"]
  customer_no = user["customer_no"]
  updated_user = f"member: {user['id']}"

  # Member not cancel account
  member_service.delete( shop_no, customer_no, updated_user)
  response = ok()
  cookie_config = make_cookie(get_member_cookie(), max_age=0)
  response.set_cookie(**cookie_config)
  return response



# Member logout function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.post("/logout", tags=["member"], dependencies=[Depends(authorized_member)])
@inject
async def logout():
  context.user.reset()
  response = ok()

  cookie_config = make_cookie(get_member_cookie(), max_age=0)
  response.set_cookie(**cookie_config)
  return response


# Check notify function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.get("/notify", tags=["member"], responses={200: {"model": CRMResponse[MemberCheckNotifyResponse]}}, dependencies=[Depends(authorized_member)])
@inject
async def check_notify(member_service: MemberService = Depends(Provide[Container.member_service])):
  user = context.user.value

  data_notifications = {"notifications" : member_service.check_notify(user["user"])}

  payload = MemberCheckNotifyResponse(**data_notifications)

  response = ok(data=payload.dict())

  return response


# Check data customer function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.get("/me", responses={200: {"model": CRMResponse[MemberLoginResponse]}}, tags=["member"], dependencies=[Depends(authorized_member)])
@inject
async def get_me(member_service: MemberService = Depends(Provide[Container.member_service])):
  user = context.user.value
  # remake token
  data_member = member_service.get_me(user["user"])
  payload = MemberLoginResponse(**data_member)
  response = ok(SUCCESS_MESSAGE.SUCMSG0010, data=payload.dict())

  cookie_config = make_cookie(get_member_cookie(), payload.token)
  response.set_cookie(**cookie_config)

  return response


# Send mail verification function
# Param:
#   @event: Data request
#   @context: Context object
# Output:
#   return: HTTP response
@member_routers.post("/{shop_no}/forget-password", tags=["member"], responses={200: {"model": CRMResponse[dict]}})
@inject
async def send_mail_forget_password(shop_no: str, body: MemberSendMailRequest, member_service: MemberService = Depends(Provide[Container.member_service])):
  result = member_service.send_mail_forget_password(body, shop_no)

  response = ok(SUCCESS_MESSAGE.SUCMSG0008, data=result)
  return response
