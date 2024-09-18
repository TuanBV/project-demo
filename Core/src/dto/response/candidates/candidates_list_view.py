"""
List candidates response model
"""

from typing import List, Optional
from pydantic import BaseModel


class CandidatesItem(BaseModel):
  """
    Candidate item
  """
  id: int
  fullname: str
  position_id: Optional[str] = None
  team_id: Optional[str] = None
  email: Optional[str] = None
  telephone_no: Optional[str] = None
  recommender_id: Optional[int] = None
  full_address: Optional[str] = None
  note: Optional[str] = None
  birthday: Optional[str] = None
  status: Optional[str] = None
  cv_file_path: Optional[str] = None
  application_date: Optional[str] = None


class InterviewItem(BaseModel):
  """
    Interview item
  """
  fullname: Optional[str] = None
  time: Optional[str] = None
  comment: Optional[str] = None
  status: Optional[str] = None
  type_kbn: Optional[str] = None


class CandidateViewResponse(BaseModel):
  candidate: Optional[CandidatesItem] = None
  list_interview: Optional[List[InterviewItem]] = None
