"""
Get action detail in print response
"""

from typing import Optional
from pydantic import BaseModel

class ActionType(BaseModel):
  id: int
  name: str
  color: str

class LoopItem(BaseModel):
  by_day: str
  count: str
  freq: str
  interval: str
  until: str

class ActionItem(BaseModel):
  """
  Action item model
  """
  id: int
  name: str
  code: str
  condition_filter_id: Optional[int] = None
  customer_tag_id: Optional[int] = None
  loop_type: LoopItem
  shop_no: str
  created_date: str
  number_of_customer: int

class ActionDetailsItem(BaseModel):
  id: int
  delivery_time: str
  body: Optional[str] = None
  pdf_frontside: Optional[str] = None
  pdf_backside: Optional[str] = None
  title: Optional[str] = None
  print_status: int
  action_note: Optional[str] = None
  number_of_customer: int

class TemplateItem(BaseModel):
  id: Optional[int] = None
  name: Optional[str] = None

class DataAction(BaseModel):
  actions: ActionItem
  action_details: ActionDetailsItem
  action_types: ActionType

class GetActionDetailPrintResponse(BaseModel):
  data_action: DataAction
  corporate_name: str
  using_history: str
