"""
Get data shop response model
"""

from typing import Optional
from pydantic import BaseModel
from helpers.kbn import (LoginNotifyFlg, PaymentMethod, PaymentPlan,
  PwChangedNotifyFlg, TwoFaFlg, TwoFaType, UserRole)

class Shop(BaseModel):
  """
  Shop model
  """
  shop_no: str
  avatar: str
  corporate_name: str
  telephone_no: str
  first_name: str
  last_name: str
  first_name_kana: str
  last_name_kana: str
  zip_code: str
  address1: str
  address2: str
  address3: str
  prefecture: str
  start_using_date: str
  contract_start_date: Optional[str] = None
  contract_end_date: Optional[str] = None
  payment_plan_kbn: PaymentPlan
  first_payment: Optional[float] = None
  monthly_payment: Optional[float] = None
  url: str
  note: str
  payment_method_code: PaymentMethod
  days_for_printing: int
  services_content: Optional[str] = None
  using_history: str

class Account(BaseModel):
  """
  Account model
  """
  id: str
  email: str
  telephone_no: str
  password_change_notification_flg: PwChangedNotifyFlg
  login_notification_flg: LoginNotifyFlg
  two_fa_flg: TwoFaFlg
  two_fa_kbn: TwoFaType
  pw_change_history: str
  last_changed_password_time: Optional[str] = None

class Owner(Account):
  role_kbn: UserRole

class Manager(Account):
  role_kbn: UserRole

class Staff(Account):
  role_kbn: UserRole

class GetShopResponse(BaseModel):
  shop: Shop
  owner: Owner
  manager:Optional[Manager] = None
  staff: Optional[Staff] = None
