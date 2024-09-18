"""
List contact candidate response model
"""

from typing import List, Optional
from pydantic import BaseModel
from helpers.kbn import (CandidateStatus)


class CandidatesItem(BaseModel):
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
  note: Optional[str] = None
  status: CandidateStatus
  cv_file_path: str
  gender: str

class ListContactCandidateResponse(BaseModel):
  item: List[CandidatesItem]
