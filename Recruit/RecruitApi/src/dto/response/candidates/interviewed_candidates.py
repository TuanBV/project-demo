"""
Interview candidate response model
"""

from typing import List
from pydantic import BaseModel
from typing import Optional
from setting import settings

class InterviewedCandidate(BaseModel):
  """
    Interviewd candidate model
  """
  id: int
  fullname: str
  email: str
  telephone_no: str
  team_id: int
  team: str
  position_id: int
  position: str
  office: str
  status: str
  mail_id: Optional[int] = None
  title: Optional[str] = None
  body: Optional[str] = None
  carbon_copy: Optional[List]
  attached_file: Optional[str] = None
  attached_file_name: Optional[str] = None
  gender: str

  def __init__(self, **data) -> None:
    """Change cv file path"""
    if data["attached_file"]:
      data["attached_file"] = f'{settings.DOMAIN_FILE}/{data["attached_file"]}'
    super().__init__(**data)


class ListInterviewedCandidateResponse(BaseModel):
  """
    List interviewd candidate model
  """
  candidates: List[InterviewedCandidate]
