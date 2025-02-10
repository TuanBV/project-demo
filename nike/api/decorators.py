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
    """
        Check role of account access for api
    """
    def permission_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if context.user.value and int(context.user.value['role']) not in roles:
                raise PermissionException(message=ERR_MESSAGE.ACCESS_DENIED)
            return func(*args, **kwargs)
        return wrapper
    return permission_decorator
