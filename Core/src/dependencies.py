"""
Dependencies
"""

import helpers.jwt as jwt
from helpers import context
from typing import Optional
from fastapi import Security
from fastapi.security import APIKeyCookie
from core import CrmUnauthorizedException, ERR_MESSAGE

api_key_admin = APIKeyCookie(name="__CRM_A", auto_error=False)
api_key_member = APIKeyCookie(name="__CRM_M", auto_error=False)
api_key_auth_two_step = APIKeyCookie(name="__CRM_S_TOKEN_TWO_AUTHEN", auto_error=False)


# Authorization
def authorized(oauth_header: Optional[str]):
  # Set token if have cookie
  if oauth_header:
    jwt_token = oauth_header
    # Verify cookies
    if len(jwt_token) > 0:
      user = jwt.verify(jwt_token)
      # Set user data to context
      context.user.set(user)

      # Return user data
      return user

  raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0042)

async def authorized_admin(
    oauth_header: Optional[str] = Security(api_key_admin)):
  user = authorized(oauth_header)

  return user

async def authorized_member(
    oauth_header: Optional[str] = Security(api_key_member)):
  user = authorized(oauth_header)

  return user

async def get_cookies_auth_two_step(
    cookies: Optional[str] = Security(api_key_auth_two_step)):
  return cookies
