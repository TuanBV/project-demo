"Shop Notify Repository"

from core import CommonRepository
from helpers import kbn
from models import ShopAccounts

class ShopAccountRepository(CommonRepository):
  """
  Repository of Shop Account
  """
  # Get shop account by id
  # Params:
  #   @shop_account_id: id of account
  # Output:
  #   return: Shop Account
  def get_shop_account_by_id(self, shop_account_id):
    with self.session_factory_read as session:
      return session.query(ShopAccounts).filter(
        ShopAccounts.id == shop_account_id,
        ShopAccounts.is_deleted == kbn.DeleteFlag.OFF.value
      ).first()


  # Update shop account by id
  # Params:
  #   @new_data: dict
  # Output:
  #   Return: Data update
  def update(self, new_data):
    with self.session_factory as session:
      updated = session.query(ShopAccounts).filter(
        ShopAccounts.id == new_data.id,
        ShopAccounts.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        "password_change_notification_flg": new_data.password_change_notification_flg,
        "login_notification_flg": new_data.login_notification_flg,
        "two_fa_flg": new_data.two_fa_flg,
        "two_fa_kbn": new_data.two_fa_kbn,
        "updated_user": f"shop_account: {new_data.updated_user}",
        "otp": new_data.otp
      })

      # Commit
      session.commit()

      return updated
