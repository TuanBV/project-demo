"""
JWWT Authenticator
"""
import jwt
import helpers.const as env
import datetime
from core.error import UnauthorizedException
from utils.date import get_current_time


def hash_token(data):
    # set time expired
    expried = get_current_time() + datetime.timedelta(seconds=env.JWT.EXPIRED)
    data['exp'] = expried.timestamp()
    # hash token & result token
    return jwt.encode(data, env.JWT.SECRET.KEY, algorithm=env.JWT.SECRET.ALGORITHM)


def verify(token):
    try:
        return jwt.decode(token, env.JWT.SECRET.KEY, algorithms=[env.JWT.SECRET.ALGORITHM])
    except jwt.ExpiredSignatureError as ese:
        raise UnauthorizedException() from ese
    except Exception as e:
        raise UnauthorizedException() from e
