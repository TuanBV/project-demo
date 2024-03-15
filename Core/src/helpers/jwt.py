"""
Authenticator
"""
import jwt
import helpers.const as env
import datetime
from core.error import CrmUnauthorizedException
from utils.date import get_current_time_obj


def hash_token(data):
  # set time expired
  expried = get_current_time_obj() + datetime.timedelta(seconds=env.JWT.EXPIRED)
  data['exp'] = expried.timestamp()
  # hash token & result token
  return jwt.encode(data, env.JWT.SECRET.KEY, algorithm=env.JWT.SECRET.ALGORITHM)


def verify(token):
  try:
    return jwt.decode(token, env.JWT.SECRET.KEY, algorithms=[env.JWT.SECRET.ALGORITHM])
  except jwt.ExpiredSignatureError as ese:
    raise CrmUnauthorizedException() from ese
  except Exception as e:
    raise CrmUnauthorizedException() from e
