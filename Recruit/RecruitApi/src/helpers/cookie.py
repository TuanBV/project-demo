"""
Cookie function
"""
from box import Box
from helpers.kbn import COOKIE_NAME
from setting import settings


def get_cookie(name: str):
  cookie = Box({
    "NAME": name,
    "DOMAIN": settings.DOMAIN_COOKIE,
    "SAMESITE": "Strict" if settings.ENVIRONMENT == "production" else "None",
    "SECURE": True if settings.ENVIRONMENT == "production" else False,
  })

  return cookie

# Get user cookie function
def get_user_cookie():
  return get_cookie(COOKIE_NAME.USER)

