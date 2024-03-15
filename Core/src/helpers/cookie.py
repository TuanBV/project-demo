"""
Cookie function
"""
from box import Box
from helpers.kbn import COOKIE_NAME
from helpers.const import IS_PROD
from setting import settings


def get_cookie(name: str):
  cookie = Box({
    "NAME": name,
    "DOMAIN": settings.DOMAIN_COOKIE,
    "SAMESITE": "Strict" if IS_PROD else "None",
    "SECURE": True if IS_PROD else False,
  })

  return cookie

# Get shop cookie function
def get_shop_cookie():
  return get_cookie(COOKIE_NAME.SHOP)

# Get admin cookie function
def get_admin_cookie():
  return get_cookie(COOKIE_NAME.ADMIN)

# Get member cookie function
def get_member_cookie():
  return get_cookie(COOKIE_NAME.MEMBER)

# Get auth two step cookie function
def get_auth_cookie():
  return get_cookie(COOKIE_NAME.TOKEN_TWO_AUTHEN)
