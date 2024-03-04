"""
List interview schedule response model
"""

from typing import List, Optional
from pydantic import BaseModel
from helpers.kbn import (CandidateStatus)


class InterviewDetailItem(BaseModel):
  employee_code: str
  fullname: str

class CandidatesItem(BaseModel):
  """
    Candidate item
  """
  id: int
  fullname: str
  position: str
  team: str
  office: str
  meeting_room_id: Optional[int] = None
  meeting_room: Optional[str] = None
  interview_form: int
  status: CandidateStatus
  cv_file_path: str
  time: str
  date: str
  employee: Optional[List[InterviewDetailItem]] = None
  gender: str

class ListInterviewScheduleResponse(BaseModel):
  item: List[CandidatesItem]
