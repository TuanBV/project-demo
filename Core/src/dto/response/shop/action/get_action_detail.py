"""
Get action detail response
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

class ActionDetailsItem(BaseModel):
  id: int
  delivery_time: str
  body: Optional[str] = None
  pdf_frontside: Optional[str] = None
  pdf_backside: Optional[str] = None
  template_id: Optional[int] = None
  title: Optional[str] = None
  print_status: int
  action_note: Optional[str] = None

class TemplateItem(BaseModel):
  id: Optional[int] = None
  name: Optional[str] = None

class GetActionDetailResponse(BaseModel):
  actions: ActionItem
  action_details: ActionDetailsItem
  action_type: ActionType
  condition_title: str
  customer_tag_title: str
  number_of_customer: Optional[int] = None
  index_action: int
  template: Optional[TemplateItem] = None
