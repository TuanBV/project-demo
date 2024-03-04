"""
Decorator
"""
from functools import wraps
from typing import List
from fastapi.security import APIKeyCookie
from helpers import context, kbn
from core import PermissionException, ERR_MESSAGE

api_key_shop = APIKeyCookie(name=kbn.COOKIE_NAME.SHOP, auto_error=False)


def permission(roles: List = None):
  def permission_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      if (context.user.value and roles and int(context.user.value["role"]) not in roles):
        raise PermissionException(message=ERR_MESSAGE.ACCESS_DENIED)
      return await func(*args, **kwargs)
    return wrapper
  return permission_decorator
