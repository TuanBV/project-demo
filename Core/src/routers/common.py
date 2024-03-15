"""
Common routers
"""

import json
import traceback
from typing import Callable
from fastapi import Request, Response, status
from fastapi.routing import APIRoute
from core.error import CrmException, CrmAppVersionException
from core.logger import (get_logger)
from core.message import ERR_MESSAGE
from helpers.common import generate_log, get_request_id
from helpers.const import CODE
from helpers import context
import helpers.jwt as jwt
from helpers.response import (make_cookie, error, ng, maintenace)
from helpers.kbn import UserRole
from helpers.cookie import get_admin_cookie, get_member_cookie, get_shop_cookie
from utils.date import format_date_time, get_current_time_obj
from setting import settings

logger = get_logger()
# Router common
class SSVRoute(APIRoute):
  """
    Route handler
  """

  # Set data cookie of user
  # Params:
  #   @user: Data user
  # Output:
  #   Return: Data cookie
  def __set_user_cookie(self, user):
    cookie = {}
    shop_no = ""
    if user["role"] == UserRole.ADMIN:
      cookie = get_admin_cookie()
      shop_no = ""
    elif user["role"] == UserRole.CUSTOMER:
      cookie = get_member_cookie()
      shop_no = user["user"]["shop_no"]
    elif user["role"] in [UserRole.SHOP_MANAGER, UserRole.SHOP_OWNER, UserRole.SHOP_STAFF]:
      cookie = get_shop_cookie()
      shop_no = user["user"]["shop_no"]

    return {
      "cookie": cookie,
      "shop_no": shop_no
    }


  # Set data response
  # Params:
  #   @response: Data response
  # Output:
  #   Return: Data user_id, shop_no, role, response
  def __set_response(self, response):
    # Get data user from context
    user_id = ""
    shop_no = ""
    role = ""
    if context.user.value:
      user = context.user.value
      # In case the response does not set cookies
      if "set-cookie" not in response.headers:
        data_cookie = {
            "user": user["user"],
            "role": user["role"]
        }
        user_id = user["user"]["id"]
        role = user["role"]

        if user["role"] not in [UserRole.ADMIN, UserRole.CUSTOMER, UserRole.SHOP_MANAGER, UserRole.SHOP_OWNER, UserRole.SHOP_STAFF]:
          raise CrmException(CODE.API.ERROR)

        data_set_cookie = self.__set_user_cookie(user)
        cookie = data_set_cookie["cookie"]
        shop_no = data_set_cookie["shop_no"]

        # Encrypt data user
        jwt_token_new = jwt.hash_token(data_cookie)
        # Status code = 401 will set cookie timeout
        cookie_config = make_cookie(cookie, jwt_token_new)
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
          cookie_config = make_cookie(cookie, jwt_token_new, max_age=0)

        # Set cookie into response
        response.set_cookie(**cookie_config)

    return {
      "user_id": user_id,
      "role": role,
      "shop_no": shop_no,
      "response": response
    }


  def __set_data_log(self):
    user_id = ""
    shop_no = ""
    role = ""
    if context.user.value:
      # Get data user from context
      user = context.user.value
      user_id = user["user"]["id"]
      role = user["role"]
      if user["role"] == UserRole.ADMIN:
        shop_no = ""
      else:
        shop_no = user["user"]["shop_no"]

    return {
      "user_id": user_id,
      "role": role,
      "shop_no": shop_no
    }


  def get_route_handler(self) -> Callable:
    original_route_handler = super().get_route_handler()

    async def custom_route_handler(request: Request) -> Response:
      user_id = ""
      shop_no = ""
      role = ""
      try:
        request_id = f"{get_request_id()}_{format_date_time(get_current_time_obj(), '%Y%m%d%H%M%S')}"
        before = get_current_time_obj()
        body_request = (await request.body()).decode()
        if body_request:
          body_request = json.loads(body_request)
        request_data = {
          "body": body_request,
          "query": request.url.query,
        }

        url_request = request.url.path
        # LOG REQUEST
        logger.info(generate_log(user_agent=request.headers.get("user-agent"), url=url_request, request_id=request_id,
                                log_type="REQUEST", method=request.method, content=request_data, time=before))

        if request.headers.get("app-version") != str(settings.APP_VERSION):
          raise CrmAppVersionException

        # process the request and get the response
        response: Response = await original_route_handler(request)
        end = get_current_time_obj()
        duration = end - before
        response.headers["X-Response-Time"] = str(duration)

        # In case the user is logged in
        data_response = self.__set_response(response)
        user_id = data_response["user_id"]
        role = data_response["role"]
        shop_no = data_response["shop_no"]
        response = data_response["response"]

        return response

      except Exception as ex:
        end = get_current_time_obj()
        if isinstance(ex, CrmException):
          error_msg = ex.message
          response = ng(ex.message, code=ex.code)
        elif isinstance(ex, CrmAppVersionException):
          response = maintenace(ex.message)
          cookie = get_admin_cookie()
          cookie_admin_config = make_cookie(cookie, max_age=0)
          cookie = get_member_cookie()
          cookie_member_config = make_cookie(cookie, max_age=0)
          cookie = get_shop_cookie()
          cookie_shop_config = make_cookie(cookie, max_age=0)
          response.set_cookie(**cookie_admin_config)
          response.set_cookie(**cookie_member_config)
          response.set_cookie(**cookie_shop_config)
          error_msg = ex.message
        else:
          response = error(ERR_MESSAGE.ERRMSG0033)
          error_msg = traceback.format_exc()

        data_log = self.__set_data_log()
        # Get data user from context
        user_id = data_log["user_id"]
        role = data_log["role"]
        shop_no = data_log["shop_no"]

        # LOG ERROR
        logger.error(generate_log(level="ERROR", user_agent=request.headers.get("user-agent"), url=url_request, request_id=request_id,
                                log_type="ERROR", method=request.method, content=error_msg, time=end, user_id=user_id, shop_no=shop_no, role=role))
        return response
      finally:
        # LOG RESPONSE
        body_response = response.body.decode()
        if body_response:
          body_response = json.loads(body_response)
        logger.info(generate_log(user_agent=request.headers.get("user-agent"), url=url_request, request_id=request_id,
                                log_type="RESPONSE", method=request.method, content=body_response, time=end, user_id=user_id, shop_no=shop_no, role=role))


    return custom_route_handler
