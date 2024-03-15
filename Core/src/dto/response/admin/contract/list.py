"""
List shop response
"""

from typing import List, Optional
from pydantic import BaseModel

from helpers.kbn import PaymentMethod, PaymentPlan


class MonthModel(BaseModel):
  value: str
  full_date: str


class ActionTypeModel(BaseModel):
  color: str
  order: str


class ActionModel(BaseModel):
  month: MonthModel
  action_type: List[ActionTypeModel]

class ShopData(BaseModel):
  """
  Shop data model
  """
  shop_no: str
  corporate_name: str
  telephone_no: str
  zip_code: str
  address1: str
  address2: str
  address3: str
  prefecture: str
  start_using_date: str
  contract_start_date: Optional[str] = None
  contract_end_date: Optional[str] = None
  payment_plan_kbn: PaymentPlan
  payment_method_code: PaymentMethod

class ShopAccountData(BaseModel):
  email: str

class ShopItem(BaseModel):
  shops: ShopData
  shop_accounts: ShopAccountData

class ListShopResponse(BaseModel):
  total_page: int
  current_page: int
  total_record: int
  item: List[ShopItem]
