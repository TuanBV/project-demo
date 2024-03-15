"Shop Account Service"

from helpers import kbn
from core import CrmUnauthorizedException, ERR_MESSAGE
import pyotp
from crm_shop_account.repository import ShopAccountRepository

class ShopAccountService:
  """
    Service of shop account
  """
  def __init__(self, shop_account_repository: ShopAccountRepository):
    self.shop_account_repo: ShopAccountRepository = shop_account_repository


  # Get shop account information
  # Param:
  #   @shop_account_id: int
  # Output:
  #   return: shop account information
  def get_shop_account(self, shop_account_id):
    shop_account = self.shop_account_repo.get_shop_account_by_id(shop_account_id)
    return shop_account


  # Edit shop account
  # Param:
  #   @data: Data request
  def edit(self, data):
    #Two-step auth check is open and is from google
    if (data.two_fa_flg == kbn.AUTH_TWO_STEP.ON and data.two_fa_kbn == kbn.AUTH_TWO_STEP_TYPE.GOOGLE):
      otp = pyotp.TOTP(data.secret_otp)
      # OPT code exists
      if not otp.verify(data.otp):
        raise CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0060)

    return self.shop_account_repo.update(data)
