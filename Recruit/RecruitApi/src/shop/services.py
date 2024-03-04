"""
SHOP Service
"""
from core import CommonException, ERR_MESSAGE
import helpers.jwt as jwt
from helpers import common
from shop import ShopRepository

class ShopService:
  """
    Service shop
  """
  def __init__(self, shop_repository: ShopRepository):
    self.shop_repo: ShopRepository = shop_repository


  # Handle login shop
  # Param:
  #   @data: Data request
  # Return: Shop information and token
  def login(self, data):
    email = data["mail"].lower()
    payload = {}
    # Execute query
    shop_account = self.shop_repo.get_shop_account_by_email(email)
    if shop_account is not None and common.checkpw(data["password"].strip(), shop_account.password):
      shop_account = shop_account.__dict__
      del shop_account["password"]
      del shop_account["token"]
      del shop_account["loginfail"]
      del shop_account["locktime"]
      del shop_account["_sa_instance_state"]

      payload["shop"] = shop_account
      payload["token"] = jwt.hash_token(shop_account)

      return payload

    # Invalid email or password
    raise CommonException(message=ERR_MESSAGE.INVALID_EMAIL_OR_PASSWORD)
