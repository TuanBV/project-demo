"""
List action child response
"""

from typing import List, Optional
from pydantic import BaseModel


class ActionDetails(BaseModel):
  id: int
  delivery_time: str
  number_of_customer: Optional[int] = None
  print_status: int
  action_code: str


class ListActionsChildResponse(BaseModel):
  total_record: int
  item: List[ActionDetails]
