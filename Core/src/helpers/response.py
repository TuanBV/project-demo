"""
Helpers response
"""

import simplejson as json
from fastapi import status
from fastapi.responses import JSONResponse
from helpers.const import (CODE, MAX_AGE)

HEADERS = {
  "Content-Type": "application/json"
}


def ok(messages="", data=None, code=CODE.API.SUCCESS):
  response = JSONResponse(
    status_code=CODE.HTTP_STATUS.SUCCESS,
    content=json.loads(json.dumps({
      "code": code,
      "message": messages,
      "payload": data
    }))
  )
  return response


def ng(messages="", code = CODE.API.ERROR, status_codes=status.HTTP_200_OK):
  response = JSONResponse(
    status_code= status_codes,
    content=json.loads(json.dumps({
      "code": code,
      "message": messages,
      "payload": None
    }))
  )
  return response


def error(messages=""):
  return ng(messages, CODE.API.SYSTEM_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)


def maintenace(messages=""):
  return ng(messages, CODE.API.APP_VERSION_ERROR, status.HTTP_503_SERVICE_UNAVAILABLE)


def make_cookie(cookie_config=None, jwt_token="", max_age=MAX_AGE):
  """
  Get the headers to add to response data
  set max_age to 0, to remove cookie
  """
  cookie = {
    "key":cookie_config.NAME,
    "value":jwt_token,
    "max_age":max_age,
    "secure":True,
    "httponly":True,
    "domain":cookie_config.DOMAIN,
    "samesite":cookie_config.SAMESITE,
    "path":"/",
  }

  return cookie
