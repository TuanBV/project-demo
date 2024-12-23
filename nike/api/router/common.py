"""
Common routers
"""

import json
import traceback
from fastapi import Depends
from typing import Callable
from fastapi import Request, Response, status
from fastapi.routing import APIRoute
from core.error import CommonException
from core.message import ERR_MESSAGE
from helpers.common import get_request_id
from helpers import context
import helpers.jwt as jwt
from helpers.response import (make_cookie, error, ng)
from helpers.cookie import get_user_cookie
from utils.date import format_date_time, get_current_time
from dependency_injector.wiring import inject, Provide
from containers import Container
from logging import Logger

# Router common
class CommonRoute(APIRoute):
  """
    Route handler
  """

  # Set data cookie of user
  # Params:
  # Output:
  #   Return: Data cookie
  def __set_user_cookie(self):
    cookie = get_user_cookie()

    return {
      "cookie": cookie,
    }


  # Set data response
  # Params:
  #   @response: Data response
  # Output:
  #   Return: Data employee_code, response
  def __set_response(self, response):
    # Get data user from context
    if context.user.value:
      user = context.user.value
      # In case the response does not set cookies
      if "set-cookie" not in response.headers:
        data_cookie = user

        data_set_cookie = self.__set_user_cookie()
        cookie = data_set_cookie["cookie"]

        # Encrypt data user
        jwt_token_new = jwt.hash_token(data_cookie)
        # Status code = 401 will set cookie timeout
        cookie_config = make_cookie(cookie, jwt_token_new)
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
          cookie_config = make_cookie(cookie, jwt_token_new, max_age=0)

        # Set cookie into response
        response.set_cookie(**cookie_config)

    return {
      "response": response
    }

  @inject
  def get_route_handler(self, logger: Logger = Depends(Provide(Container.logger))) -> Callable:
    original_route_handler = super().get_route_handler()

    async def custom_route_handler(request: Request) -> Response:
      try:
        request_id = f"{get_request_id()}_{format_date_time(get_current_time(), '%Y%m%d%H%M%S')}"
        before = get_current_time()
        body_request = (await request.body()).decode()
        if body_request:
          body_request = json.loads(body_request)
        request_data = {
          "body": body_request,
          "query": request.url.query,
        }

        url_request = request.url.path
        # LOG REQUEST
        # logger.request(url_request, request_id, request.method, request.headers.get("user-agent"), request_data)

        # process the request and get the response
        response: Response = await original_route_handler(request)
        end = get_current_time()
        duration = end - before
        response.headers["X-Response-Time"] = str(duration)

        # In case the user is logged in
        data_response = self.__set_response(response)
        response = data_response["response"]

        return response

      except Exception as ex:
        if isinstance(ex, CommonException):
          error_msg = ex.message
          response = ng(ex.message, code=ex.code)
        else:
          response = error(ERR_MESSAGE.SERVER_ERROR)
          error_msg = traceback.format_exc()

        # LOG ERROR RESPONSE
        # logger.err_response(url_request, request_id, request.method, request.headers.get("user-agent"), error_msg)

        return response
      finally:
        # LOG RESPONSE
        body_response = response.body.decode()
        if body_response:
          body_response = json.loads(body_response)

        # LOG RESPONSE
        # logger.response(url_request, request_id, request.method, request.headers.get("user-agent"), body_response)

    return custom_route_handler
