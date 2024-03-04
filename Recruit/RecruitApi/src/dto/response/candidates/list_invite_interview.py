"""
List invite interview response model
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
  interview_form: Optional[int] = None
  status: CandidateStatus
  time: Optional[str] = None
  mail_id: Optional[int] = None
  title: Optional[str] = None
  body: Optional[str] = None
  carbon_copy: Optional[List] = None
  date: Optional[str] = None
  gender: str

class ListInviteInterviewResponse(BaseModel):
  item: List[CandidatesItem]
