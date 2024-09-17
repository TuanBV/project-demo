"""
Service owner repository
"""

from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from core import CommonRepository
# from models import Customers, PaymentMethods, SettingRanks, ShopAccounts, Shops, SiteConfigs, Templates
from helpers import kbn
from utils.date import get_current_time_obj

del_flg_off = kbn.DeleteFlag.OFF.value

class UserRepository(CommonRepository):
  """
  Repository of Service user
  """


  # Get data user by id
  # Params:
  #   @user_id: id of user
  # Output:
  #   return: user item
  def get_user(self, user_id):
    with self.session_factory_read() as session:
      # result = session.query(ShopAccounts).filter(
      #   ShopAccounts.id == shop_account_id,
      #   ShopAccounts.is_deleted == del_flg_off
      # ).first()

      return 1


  # # Get data shop account by email
  # # Params:
  # #   @email: email of shop
  # # Output:
  # #   return: Shop account item
  # def get_shop_account_by_email(self, email):
  #   with self.session_factory_read() as session:
  #     result = session.query(ShopAccounts).filter(
  #       ShopAccounts.email == email,
  #       ShopAccounts.is_deleted == del_flg_off
  #     ).first()

  #     return result


  # # Get data shop by shop_no
  # # Params:
  # #   @shop_no: Shop no of shop
  # # Output:
  # #   return: Shop item
  # def get_shop(self, shop_no):
  #   with self.session_factory_read() as session:
  #     result = session.query(Shops).filter(
  #       Shops.shop_no == shop_no,
  #       Shops.is_deleted == del_flg_off
  #     ).first()

  #     return result


  # # Get data setting rank by shop_no
  # # Params:
  # #   @shop_no: Shop no of shop
  # # Output:
  # #   return: Setting rank item
  # def get_setting_rank(self, shop_no):
  #   with self.session_factory_read() as session:
  #     result = session.query(SettingRanks).filter(
  #       SettingRanks.shop_no == shop_no,
  #       SettingRanks.is_deleted == del_flg_off
  #     ).first()

  #     return result


  # # Get data template by shop_no
  # # Params:
  # #   @shop_no: shop_no of shop
  # # Output:
  # #   return: List template of shop
  # def get_template_by_id(self, shop_no):
  #   with self.session_factory_read() as session:
  #     # Execute data template by shop_no
  #     response_templates = session.query(Templates).filter(
  #       Templates.shop_no == shop_no,
  #       Templates.is_deleted == del_flg_off,
  #       or_(
  #         Templates.key == "member_register_success",
  #         Templates.key == "member_forgot_password",
  #         Templates.key == "member_forgot_password",
  #         Templates.key == "member_reset_password",
  #         Templates.key == "member_edit_success",
  #         Templates.key == "member_unsubscribe_success",
  #         Templates.key == "customer_register_success",
  #         Templates.key == "customer_edit_success"
  #       )
  #     ).all()

  #     # Get dict template mail
  #     template_mail = {}
  #     for template in response_templates:
  #       template_mail[template.key] = template.id

  #     # Data return
  #     return template_mail


  # # Get data shop account by shop_no
  # # Params:
  # #   @shop_no: shop_no of shop
  # # Output:
  # #   return: List shop account has role manager or owner
  # def get_manager_owner(self, shop_no):
  #   with self.session_factory_read() as session:
  #     # Execute data template by shop_no
  #     result_shop_account = jsonable_encoder(session.query(ShopAccounts).filter(
  #       ShopAccounts.shop_no == shop_no,
  #       ShopAccounts.is_deleted == del_flg_off,
  #       or_(
  #         ShopAccounts.role_kbn == kbn.UserRole.SHOP_MANAGER.value,
  #         ShopAccounts.role_kbn == kbn.UserRole.SHOP_OWNER.value
  #       )
  #     ).all())

  #     return result_shop_account


  # # Get data payment method
  # # Params:
  # #    @payment_method_code: code of payment method
  # # Output:
  # #   return: Payment method item
  # def get_payment_method(self, payment_method_code):
  #   with self.session_factory_read() as session:
  #     result_payment_method = session.query(PaymentMethods).filter(
  #       PaymentMethods.is_deleted == del_flg_off,
  #       PaymentMethods.code == payment_method_code
  #     ).first()

  #     return result_payment_method


  # # Get data list mail admin from site config table
  # # Params:
  # # Output:
  # #   return: List mail admin
  # def get_site_config(self):
  #   with self.session_factory_read() as session:
  #     mail_admin = []
  #     # Get list mail admin
  #     result = session.query(SiteConfigs).filter(SiteConfigs.key == "mail_admin").all()
  #     for item in result:
  #       mail_admin.append(item.value)

  #     return mail_admin


  # # Get country code from site config
  # # Params:
  # # Output:
  # #   return: country code item
  # def get_country_code(self):
  #   with self.session_factory_read() as session:
  #     # Get COUNTRY_CODE
  #     result_country_code = session.query(SiteConfigs).filter(SiteConfigs.key == "COUNTRY_CODE").first()

  #     return result_country_code


  # # Update shop account
  # # Param:
  # #   @account: account
  # # Output: Void
  # def update(self, account):
  #   with self.session_factory() as session:
  #     # Update data shop account
  #     session.query(ShopAccounts).filter(ShopAccounts.id == account["id"]).update({"secret_otp": account["secret_otp"]})

  #     # Commit
  #     session.commit()


  # # Update token and token_expiration_time of shop account
  # # Param:
  # #   @email: email of shop account
  # #   @token: token new of shop
  # #   @token_expiration_time: token_expiration_time of shop account
  # # Output: Void
  # def update_shop_account_forgot_pw(self, email, token, token_expiration_time):
  #   with self.session_factory() as session:
  #     # Update data shop account
  #     data_update = {
  #       "token": token,
  #       "token_expiration_time": token_expiration_time,
  #     }

  #     # Get shop account by email
  #     result_shop_account = session.query(ShopAccounts).filter(ShopAccounts.email == email).first()

  #     # Update data shop account
  #     session.query(ShopAccounts).filter(ShopAccounts.id == result_shop_account.id).update(data_update)

  #     # Commit
  #     session.commit()


  # # Update password new for shop account
  # # Param:
  # #   @password: password new of shop
  # #   @shop_account_id: id of shop
  # #   @user_update: user update password
  # # Output: Void
  # def update_password(self, shop_account_id, password, user_update):
  #   with self.session_factory() as session:
  #     # Update data shop account
  #     session.query(ShopAccounts).filter(
  #       ShopAccounts.id == shop_account_id
  #     ).update({
  #         "password": password,
  #         "last_changed_password_time": get_current_time_obj().strftime("%Y/%m/%d %H:%M:%S"),
  #         "updated_user": f"shop_account: {user_update}",
  #         "token_expiration_time": None,
  #         "token": None
  #     })

  #     # Commit
  #     session.commit()


  # # Update otp of shop account
  # # Param:
  # #   @email: email of shop account
  # #   @otp: otp of shop account
  # # Output: Void
  # def update_otp_shop_account(self, email, otp):
  #   with self.session_factory() as session:
  #     # Get shop account by email
  #     result_shop_account = session.query(ShopAccounts).filter(ShopAccounts.email == email).first()
  #     # Update data shop account
  #     session.query(ShopAccounts).filter(ShopAccounts.id == result_shop_account.id).update({"otp": otp})

  #     # Commit
  #     session.commit()


  # # Update security
  # # Param:
  # #   @shop_account_id: id of shop account
  # #   @otp: otp of shop account
  # # Output: Void
  # def update_security(self, shop_account_id, data):
  #   with self.session_factory() as session:
  #     # Update data shop account
  #     session.query(ShopAccounts).filter(ShopAccounts.id == shop_account_id).update(data)

  #     # Commit
  #     session.commit()


  # # Param:
  # #  @email: shop account information
  # #  @shop_no: shop_no of shop
  # #  @customer_no: customer_no of account
  # # Output:
  # #  return: boolean
  # def check_customer_exist(self, email, shop_no, customer_no=""):
  #   with self.session_factory_read() as session:
  #     account = session.query(Customers).filter(
  #       Customers.email == email,
  #       Customers.shop_no == shop_no,
  #       Customers.is_deleted == kbn.DeleteFlag.OFF.value
  #     ).first()

  #     # Check customer_no
  #     if customer_no and account:
  #       if account.customer_no != customer_no:
  #         return False

  #     # If there is data with the email entered
  #     # it will return an error
  #     if not customer_no and account:
  #       return False
  #     return True


  # # Verify token
  # # Param:
  # #  @token: Token
  # # Output:
  # #  return: boolean
  # def verify_token(self, token):
  #   with self.session_factory_read() as session:
  #     result = session.query(ShopAccounts).filter(
  #       ShopAccounts.token == token,
  #       ShopAccounts.is_deleted == kbn.DeleteFlag.OFF.value
  #     ).first()

  #     # Token not exist
  #     if result is None:
  #       return False
  #     return True


  # # Check password_new and confirm_password is the same
  # # Param:
  # #  @password_new: password new
  # #  @confirm_password: confirm password
  # # Output: boolean
  # def check_match_password(self, confirm_password, password_new):
  #   # Token not exist
  #   if confirm_password != password_new:
  #     return False

  #   return True
