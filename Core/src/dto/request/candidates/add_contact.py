"""
Add contact request model
"""

from typing import Optional
from pydantic import BaseModel, Field
from helpers.const import REGEXP_NUMBER


class FileItem(BaseModel):
  file: str
  file_ext: str
  file_size: str


class AddContactRequest(BaseModel):
  """
  Add contact request model
  """
  time: str = Field(..., title="Time interview", min_length=1)
  link_interview: Optional[str] = Field(None, title="Link interview")
  interview_form: Optional[str] = Field(..., title="Type interview form", pattern="^[1-2]{1}$")
  note: Optional[str] = Field(None, title="Note")
  office_id: Optional[str] = Field(..., title="Office id", pattern=REGEXP_NUMBER, min_length=1)
  candidate_id: str
  date: str = Field(..., title="Date interview", min_length=1)
