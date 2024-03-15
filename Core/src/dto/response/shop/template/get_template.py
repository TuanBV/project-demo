"""
Get template response
"""

from typing import Optional
from pydantic import BaseModel


class ActionType(BaseModel):
  id: int
  name: str
  color: str

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
  key: Optional[str] = None

class GetTemplatesResponse(BaseModel):
  action_type: ActionType
  template: TemplateItem
