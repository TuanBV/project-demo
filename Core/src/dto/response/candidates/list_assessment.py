"""
List assessment response model
"""

from typing import List, Optional
from pydantic import BaseModel
from helpers.kbn import (CandidateStatus, Evaluate)


class InterviewDetailItem(BaseModel):
  id: int
  employee_code: str
  fullname: str
  comment: Optional[str] = None
  evaluate: Evaluate

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
  status: CandidateStatus
  meeting_room: Optional[str] = None
  employee: Optional[List[InterviewDetailItem]] = None
  time: str
  date: str
  gender: str

class ListAssessmentResponse(BaseModel):
  item: List[CandidatesItem]
