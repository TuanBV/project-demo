"""
Shop login model
"""

from pydantic import BaseModel
from typing import List, Optional

class DataActionType(BaseModel):
  icon: str
  id: int
  name: str
  color: str
  comment: str
  is_deleted: str
  sort_order_no: str

class DataCampaign(BaseModel):
  comment: str
  end_date: str
  point: str
  start_date: str

class DataAddress(BaseModel):
  address1: str
  address2: str
  address3: str
  pref: str

class DataSettingRank(BaseModel):
  rank_a: Optional[str] = None
  rank_b: Optional[str] = None
  rank_c: Optional[str] = None
  rank_s: Optional[str] = None
  range_date: int
  kbn: Optional[int] = None


class DataTemplateMail(BaseModel):
  customer_edit_success: str
  customer_register_success: str
  member_edit_success: str
  member_forgot_password: str
  member_register_success: str
  member_reset_password: str
  member_unsubscribe_success: str

class DataShop(BaseModel):
  """
  Properties
  """
  first_name: str
  first_name_kana: str
  last_name: str
  last_name_kana: str
  payment_method_code: str
  address1: str
  address2: str
  address3: str
  prefecture: str
  logo: str
  name: str
  shop_no: str
  zip_code: str
  contract_end_date: Optional[str] = None
  contract_start_date: Optional[str] = None
  corporate_name: str
  avatar: str
  payment_plan_kbn: int
  monthly_payment: Optional[float] = None
  days_for_printing: str
  start_using_date: str
  action_type: List[DataActionType]
  template_mail: DataTemplateMail
  setting_rank: DataSettingRank
  campaign_start_date: Optional[str] = None
  campaign_end_date: Optional[str] = None
  campaign_point: Optional[int] = None
  campaign_note: Optional[str] = None
  point_default: Optional[int] = None
  url: str
  telephone_no: str
  slogan: Optional[str] = None
  color: Optional[str]
  flag_prepare_data_action: str

class ShopUser(BaseModel):
  """
  Properties
  """
  two_fa_flg: int
  two_fa_kbn: int
  email: str
  secret_otp: str
  role_kbn: int
  last_changed_password_time: Optional[str] = None
  password_change_history: Optional[str] = None
  password_change_notification_flg: str
  login_notification_flg: str
  id: int
  uri_qr_code_otp: str
  shop: DataShop


class ShopLoginResponse(BaseModel):
  role: int
  token: str
  user: ShopUser
