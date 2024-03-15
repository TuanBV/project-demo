"""
  Response of edit customer
"""
from typing import Optional
from pydantic import BaseModel

class CustomerInformation(BaseModel):
  """
  Properties
  """
  amount_1_month: float
  amount_3_month: float
  amount_6_month: float
  amount_12_month: float
  visited_1_month: int
  visited_3_month: int
  visited_6_month: int
  visited_12_month: int
  range_date_registered: str
  range_date_visited: str

class Customer(BaseModel):
  """
    Properties
  """
  last_name: str
  telephone_no: Optional[str] = None
  avatar: str
  shop_no: str
  last_name_kana: str
  total_amount: float
  first_name: str
  registered_date: str
  email: str
  zip_code: str
  last_visited_date: Optional[str] = None
  customer_no: str
  address1: str
  address2: str
  address3: str
  prefecture: str
  rank: int
  rank_kbn: int
  first_name_kana: str
  note: Optional[str] = None
  sex_kbn: int
  points: str
  birthday: str
  total_visits: int
  is_deleted: int
  subscription_flag: int

class EditCustomerResponse(BaseModel):
  customers: Customer
  customer_informations: CustomerInformation
