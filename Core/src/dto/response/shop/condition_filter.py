"""
Condition filter model
"""

from typing import List
from pydantic import BaseModel

# Add condition filter model
class ExtendedSearch(BaseModel):
  """
  Properties
  """
  rank: str
  sex_type: str
  age_from: str
  age_to: str
  birthday: str
  points_from: str
  points_to: str
  zip_code_from: str
  zip_code_to: str
  registered_date: str
  registered_date_from: str
  registered_date_to: str
  last_visited_date: str
  range_date_visited_from: str
  range_date_visited_to: str
  amount_1_month_from: str
  amount_1_month_to: str
  amount_3_month_from: str
  amount_3_month_to: str
  amount_6_month_from: str
  amount_6_month_to: str
  amount_12_month_from:str
  amount_12_month_to: str
  total_amount_from: str
  total_amount_to: str
  visited_1_month_from: str
  visited_1_month_to: str
  visited_3_month_from: str
  visited_3_month_to: str
  visited_6_month_from: str
  visited_6_month_to: str
  visited_12_month_from: str
  visited_12_month_to: str
  total_visits_from: str
  total_visits_to: str
  subscription_flag: str
  is_deleted: int

class ExclusionSearch(BaseModel):
  range_date_act_future: str
  range_date_act_sent: str
  range_date_visited: str
  action_type: int

class FilterDetail(BaseModel):
  extended_search: ExtendedSearch
  exclusion_search: ExclusionSearch
  search_key: str

class AddConditionFilterResponse(BaseModel):
  title: str
  customer_filters: FilterDetail

# List condition filter model
class DataCondition(BaseModel):
  id: int
  customer_filters: FilterDetail
  shop_no: str
  title: str

class ConditionFilterResponse(BaseModel):
  item: List[DataCondition]

class NumberOfCustomerResponse(BaseModel):
  total_record: int

