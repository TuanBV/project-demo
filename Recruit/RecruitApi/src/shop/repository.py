"""
Service owner repository
"""

from core import CommonRepository
from models import Shop

class ShopRepository(CommonRepository):
  """
  Repository of Service shop
  """


  # Get shop by email
  # Params:
  #   @email: email of shop
  # Output:
  #   return: Shop account
  def get_shop_account_by_email(self, email):
    with self.session_factory_read() as session:
      result = session.query(Shop).filter(
        Shop.mail == email,
      ).first()

      return result
