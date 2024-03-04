"""
Add interview information request model
"""

from typing import Optional, List
from pydantic import BaseModel, Field

class AddInterviewInforRequest(BaseModel):
  """
  Add contact request model
  """
  time: str = Field(..., title="Time interview", min_length=1)
  meeting_room: Optional[str] = Field(..., title="Type interview")
  date: str = Field(..., title="Date interview", min_length=1)
  employee: Optional[List[str]]


class EditInterviewInforRequest(BaseModel):
  """
  Edit contact request model
  """
  time: str = Field(..., title="Time interview", min_length=1)
  meeting_room: Optional[str] = Field(..., title="Type interview")
  date: str = Field(..., title="Date interview", min_length=1)
  employee: Optional[List[str]]
  flag_not_interview: bool
