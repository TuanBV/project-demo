"""
List action response
"""

from typing import List, Optional
from pydantic import BaseModel

class ActionType(BaseModel):
  id: int
  name: str
  color: str

class ActionItem(BaseModel):
  """
  Action item model
  """
  id: int
  name: str
  code: str
  shop_no: str
  number_of_customer: int

class ShopItem(BaseModel):
  id: int
  corporate_name: str
  shop_no: str

class ActionDetailItem(BaseModel):
  id: int
  delivery_time: str
  number_of_customer: Optional[int] = None
  print_status: int
  action_code: str

class ItemData(BaseModel):
  actions: ActionItem
  action_details: ActionDetailItem
  action_types: ActionType
  shops: ShopItem
  flag_check_deadline: bool

class ListActionDetailsResponse(BaseModel):
  total_page: int
  current_page: int
  total_record: int
  item: List[ItemData]
