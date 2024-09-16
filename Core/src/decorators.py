"""
Decorator
"""
from functools import wraps
from typing import List
from fastapi.security import APIKeyCookie
from helpers import context
from core import PermissionException, ERR_MESSAGE

api_key_admin = APIKeyCookie(name="__Information_A", auto_error=False)


def permission(roles: List = None):
  def permission_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      if (context.user.value and roles and int(context.user.value["role"]) not in roles):
        raise PermissionException(message=ERR_MESSAGE.ERRMSG0179)
      return await func(*args, **kwargs)
    return wrapper
  return permission_decorator
