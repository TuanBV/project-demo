"""
Get customer by customer no model
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel


class Address(BaseModel):
  address_line_1: str
  address_line_2: str
  address_line_3: str
  pref: str


class Month(BaseModel):
  value: str
  full_date: str


class AllListCustomerTagsItem(BaseModel):
  title: str
  id: int


class AllListCustomerTagsByIdItem(BaseModel):
  id: int
  title: str


class ArrayMonthItem(BaseModel):
  value: str
  full_date: str


class ActionType(BaseModel):
  sort_order_no: int
  icon: str
  comment: str
  name: str
  color: str


class ListActionItem(BaseModel):
  """
  Properties
  """
  name: Optional[str] = None
  code: Optional[str] = None
  shop_no: str
  action_types: ActionType
  action_type_id: Optional[int] = None
  title: Optional[str] = None
  body: Optional[str] = None
  template_id: Optional[str] = None
  action_detail_id: Optional[int] = None
  delivery_time: Optional[str] = None
  changed_date: Optional[str] = None
  description: Optional[str] = None
  note: Optional[str] = None
  payment: Optional[str] = None
  points: Optional[str] = None
  id: Optional[int] = None


class ActionTypeItem1(BaseModel):
  color: str
  sort_order_no: str


class DayCalendarItem(BaseModel):
  delivery_date: Optional[str] = None
  action_type_name: Optional[List[str]] = None

class MonthCalendarItem(BaseModel):
  month: Optional[str] = None
  action_type: Optional[List[ActionTypeItem1]] = None
  year: Optional[str] = None

class ActionTypeItem(BaseModel):
  color: Optional[str] = None
  sort_order_no: Optional[str] = None

class ItemAction(BaseModel):
  month: ArrayMonthItem
  action_type: Optional[List[ActionTypeItem]]

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
  actions_by_month: List[ItemAction]
  seniority: str
  gender: str

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
  sex_kbn: str
  points: int
  birthday: str
  total_visits: int

class ListAction(BaseModel):
  action_type: str
  delivery_time: str

class CalendarItem(BaseModel):
  list_act: Optional[List[ListAction]] = None
  list_month: List[MonthCalendarItem]
class DashboardCustomerResponse(BaseModel):
  """
  Properties
  """
  customers: Customer
  customer_informations: CustomerInformation
  all_list_customer_tags: Optional[List[AllListCustomerTagsItem]] = None
  list_customer_tag_by_customer_no: Optional[List[AllListCustomerTagsByIdItem]] = None
  list_action: Optional[List[ListActionItem]] = None
  list_action_calendar: Optional[CalendarItem] = None
  array_month: Optional[List[Month]] = None
  flag_prepare_data_act: Optional[str] = None

class ActionByDateResponse(BaseModel):
  list_action: List[ListActionItem]
  list_action_calendar: CalendarItem
  array_month: Optional[List[Month]] = None
  all_list_customer_tags: List[AllListCustomerTagsItem]


class ItemActionByMonth(BaseModel):
  action_type_id: int
  delivery_time: str
  action_type: str


class ActionByMonthResponse(BaseModel):
  item: Optional[List[ItemActionByMonth]] = None
