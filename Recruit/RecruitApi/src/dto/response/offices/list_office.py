"""
Offices response
"""

from pydantic import BaseModel
from typing import List, Optional

class ItemOffice(BaseModel):
  """
    Response of office
  """
  id: int
  name: str

class ListOfficeResponse(BaseModel):
  list_office: Optional[List[ItemOffice]]= None

