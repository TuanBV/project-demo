"""
List add cv response model
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
  recommender: Optional[str] = None
  status: CandidateStatus
  previous_status: Optional[CandidateStatus] = None
  application_date: str
  cv_file_path: str
  gender: str

class ListAddCvResponse(BaseModel):
  item: List[CandidatesItem]
