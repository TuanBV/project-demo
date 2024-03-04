"""
Eliminate test request model
"""

from typing import Optional, List
from pydantic import BaseModel


class CandidateItem(BaseModel):
  id: int
  flag_not_test: bool


class EliminateAllTestRequest(BaseModel):
  """
  Eliminate all test request model
  """
  list_id: Optional[List[CandidateItem]]
