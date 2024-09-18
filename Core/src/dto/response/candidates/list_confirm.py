"""
List confirm test response model
"""

from typing import List, Optional
from pydantic import BaseModel


class CandidatesItem(BaseModel):
  """
    Candidate item
  """
  id: int
  fullname: str
  email: str
  telephone_no: str
  team: str
  office: str
  score: Optional[int] = None
  interview_id: int
  gender: str


class ListConfirmTestResponse(BaseModel):
  item: List[CandidatesItem]
