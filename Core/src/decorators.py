"""
Decorator
"""
from functools import wraps
from typing import List
from fastapi.security import APIKeyCookie
from helpers import context
from core import CrmPermissionException, ERR_MESSAGE

api_key_admin = APIKeyCookie(name="__CRM_A", auto_error=False)
api_key_shop = APIKeyCookie(name="__CRM_S", auto_error=False)
api_key_member = APIKeyCookie(name="__CRM_M", auto_error=False)


def permission(roles: List = None):
  def permission_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      if (context.user.value and roles and int(context.user.value["role"]) not in roles):
        raise CrmPermissionException(message=ERR_MESSAGE.ERRMSG0179)
      return await func(*args, **kwargs)
    return wrapper
  return permission_decorator
