"""
Confirm all test request model
"""

from typing import Optional, List
from pydantic import BaseModel


class ConfirmAllTestRequest(BaseModel):
  """
  Confirm all test request model
  """
  list_id: Optional[List[int]]
