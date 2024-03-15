"""
Response customer
"""

from typing import List, Optional
from pydantic import BaseModel
from dto.response.shop import FilterDetail

class MonthModel(BaseModel):
  value: str
  full_date: str

class ActionTypeModel(BaseModel):
  color: Optional[str] = None
  sort_order_no: Optional[str] = None


class ActionModel(BaseModel):
  month: MonthModel
  action_type: Optional[List[ActionTypeModel]] = []

class CustomerInformation(BaseModel):
  """
  Properties
  """
  actions_by_month: List[ActionModel]

class Customer(BaseModel):
  """
  Properties
  """
  id: int
  last_name: str
  last_name_kana: str
  first_name: str
  first_name_kana: str
  telephone_no: Optional[str] = None
  shop_no: str
  email: str
  zip_code: str
  customer_no: str
  rank: int
  birthday: str
  registered_date: str


class ItemItem(BaseModel):
  """
  Properties
  """
  customers: Customer
  customer_informations: CustomerInformation


class ListCustomerResponse(BaseModel):
  total_page: int
  current_page: int
  total_record: int
  item: List[ItemItem]
  condition: Optional[FilterDetail] = None
  list_customer_no: Optional[List[str]] = None
  flag_prepare_data_act: str


class ExportCSVResponse(BaseModel):
  item: str
