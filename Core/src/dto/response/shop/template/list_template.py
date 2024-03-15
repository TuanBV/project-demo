"""
List template response
"""

from typing import List, Optional
from pydantic import BaseModel

class ActionType(BaseModel):
  id: int
  name: str


class TemplateItem(BaseModel):
  """
  Template item model
  """
  id: int
  name: str
  title: Optional[str] = None
  shop_no: str
  comment: Optional[str] = None
  note: Optional[str] = None
  thumbnail: Optional[str] = None
  content: Optional[str] = None
  pdf_frontside: Optional[str] = None
  pdf_backside: Optional[str] = None

class ItemData(BaseModel):
  action_types: ActionType
  templates: TemplateItem

class ListTemplatesResponse(BaseModel):
  total_page: int
  current_page: int
  total_record: int
  item: List[ItemData]
