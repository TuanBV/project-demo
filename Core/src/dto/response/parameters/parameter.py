"""
Parameter response
"""

from pydantic import BaseModel
from typing import Optional, List

class ParameterResponse(BaseModel):
  """
    Response of parameter
  """
  id: str
  name: str
  table: str
  column: str
  note: Optional[str] = None

class ItemParameter(BaseModel):
  """
    Response of item parameter
  """
  id: str
  name: str
  note: Optional[str] = None

class ListParameterResponse(BaseModel):
  """
    Response of list parameter
  """
  list_param: Optional[List[ItemParameter]] = None
  count: int
