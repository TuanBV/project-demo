"""
Condition filter model
"""
from typing import Optional
from pydantic import BaseModel, Field
import helpers.const as env

# Condition filter model
class ExtendedSearch(BaseModel):
  """
  Extended search model
  """
  rank: Optional[str] = Field(regex="^[1-4]{1}$|^$", default="")
  sex_type: Optional[str] = Field(regex="^[1-3]{1}|^$", default="")
  age_from: Optional[str] = Field(regex=env.REGEXP.YEAR, default="")
  age_to: Optional[str] = Field(regex=env.REGEXP.YEAR, default="")
  birthday: Optional[str] = Field(regex="^(0[1-9]|1[0-2])$|^$", default="")
  points_from: Optional[str] = Field(regex="^[0-9](\\d{0,6})$|^$", default="")
  points_to: Optional[str] = Field(regex="^[0-9](\\d{0,6})$|^$", default="")
  zip_code_from: Optional[str] = Field(regex="^[0-9]{7}$|^$", default="")
  zip_code_to: Optional[str] = Field(regex="^[0-9]{7}$|^$", default="")
  registered_date: Optional[str] = Field(regex="^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$|^$", default="")
  registered_date_from: Optional[str] = Field(regex=env.REGEXP.YEAR, default="")
  registered_date_to: Optional[str] = Field(regex=env.REGEXP.YEAR, default="")
  last_visited_date: Optional[str] = Field(regex="^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$|^$", default="")
  range_date_visited_from: Optional[str] = Field(regex=env.REGEXP.YEAR, default="")
  range_date_visited_to: Optional[str] = Field(regex=env.REGEXP.YEAR, default="")
  amount_1_month_from: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  amount_1_month_to: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  amount_3_month_from: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  amount_3_month_to: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  amount_6_month_from: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  amount_6_month_to: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  amount_12_month_from:Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  amount_12_month_to: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  total_amount_from: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  total_amount_to: Optional[str] = Field(regex=env.REGEXP.AMOUNT, default="")
  visited_1_month_from: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  visited_1_month_to: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  visited_3_month_from: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  visited_3_month_to: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  visited_6_month_from: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  visited_6_month_to: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  visited_12_month_from: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  visited_12_month_to: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  total_visits_from: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  total_visits_to: Optional[str] = Field(regex=env.REGEXP.VISIT, default="")
  subscription_flag: Optional[str] = Field(regex="^[0-1]{1}$|^$", default="")
  is_deleted: Optional[str] = Field(regex="^[0-1]{1}$|^$", default="0")

class ExclusionSearch(BaseModel):
  range_date_act_future: Optional[str] = Field(regex=env.REGEXP.RANGE_DATE, default="")
  range_date_act_sent: Optional[str] = Field(regex=env.REGEXP.RANGE_DATE, default="")
  range_date_visited: Optional[str] = Field(regex=env.REGEXP.RANGE_DATE, default="")
  action_type: Optional[int] = Field(ge=0, le=4, default=0)

class FilterDetail(BaseModel):
  extended_search: ExtendedSearch
  exclusion_search: ExclusionSearch
  search_key: Optional[str] = Field(max_length=100, default="")

class AddConditionFilterRequest(BaseModel):
  """
    Properties and validator
  """
  filter_detail: FilterDetail
  title: Optional[str] = Field(max_length=100)
