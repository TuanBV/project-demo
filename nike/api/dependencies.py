"""
Dependencies
"""

import helpers.jwt as jwt
from helpers import context
from typing import Optional
from fastapi import Security
from fastapi.security import APIKeyCookie
from core import UnauthorizedException, ERR_MESSAGE

api_key_user = APIKeyCookie(name="__USER", auto_error=False)

# Authorization
def authorized(oauth_header: Optional[str]):
    """
        Verify JWT token and return user data
    """
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
    raise UnauthorizedException(message=ERR_MESSAGE.UNAUTHENTICATION)

async def authorized_user(oauth_header: Optional[str] = Security(api_key_user)):
    """
        Verify JWT token and return user data
    """
    user = authorized(oauth_header)
    return user
