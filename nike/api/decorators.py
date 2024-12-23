"""
Decorator
"""
from functools import wraps
from typing import List
from fastapi.security import APIKeyCookie
from helpers import context, kbn
from core import PermissionException, ERR_MESSAGE

api_key_user = APIKeyCookie(name=kbn.COOKIE_NAME.USER, auto_error=False)


def permission(roles: List = None):
    def permission_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if (context.user.value and roles):
                raise PermissionException(message=ERR_MESSAGE.ACCESS_DENIED)
            return await func(*args, **kwargs)
        return wrapper
    return permission_decorator
