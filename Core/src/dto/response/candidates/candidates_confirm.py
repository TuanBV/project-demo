"""
List candidates response model
"""

from typing import List, Optional
from pydantic import BaseModel


class CandidatesConfirmItem(BaseModel):
  """
    Candidate item
  """
  id: int
  fullname: str
  email: str
  telephone_no: str
  position: str
  team: str
  office: str
  status: Optional[str]
  gender: str

class CandidatesConfirmListResponse(BaseModel):
  item: Optional[List[CandidatesConfirmItem]] = None
