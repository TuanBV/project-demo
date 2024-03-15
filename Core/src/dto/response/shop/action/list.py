"""
List action response
"""

from typing import List, Optional
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
  first_delivery_time: str
  number_of_customer: int

class ItemData(BaseModel):
  actions: ActionItem
  action_types: ActionType

class ListActionsResponse(BaseModel):
  total_page: int
  current_page: int
  total_record: int
  item: List[ItemData]
