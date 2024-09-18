"""
Templates response
"""

from pydantic import BaseModel
from typing import Optional, List

class TemplateResponse(BaseModel):
  """
    Response of templates
  """
  id: str
  title: str
  body: str
  note: Optional[str] = None


class ListTemplateResponse(BaseModel):
  """
    Response of list templates
  """
  list_templates: Optional[List[TemplateResponse]] = None
  count: int
