"""
Get shop user model
"""
from pydantic import BaseModel
from typing import List

# Me model
class RankPurchase(BaseModel):
  rank_a: str
  rank_s: str
  rank_b: str
  rank_c: str

class AmountPurchase(BaseModel):
  range_date: str
  rank: RankPurchase

class RankVisit(BaseModel):
  rank_a_visit: str
  rank_s_visit: str
  rank_b_visit: str
  rank_c_visit: str

class NumberVisit(BaseModel):
  range_date: str
  rank: RankVisit

class Setting(BaseModel):
  number_visit: NumberVisit
  amount_purchase: AmountPurchase

class Address(BaseModel):
  address_line_1: str
  address_line_2: str
  address_line_3: str
  pref: str

class Shop(BaseModel):
  template_mail: List[str]
  shop_id: str
  setting_rank: Setting
  url_shop: str
  address: Address
  telephone_no: str
  corporate_name: str

class User(BaseModel):
  shop_account_id: str
  shop_no: str
  mail_address: str
  role: str
  exp: str
  shop: Shop

class ShopUserRequest(BaseModel):
  user: User
