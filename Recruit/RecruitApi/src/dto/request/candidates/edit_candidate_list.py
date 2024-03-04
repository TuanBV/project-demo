"""
Edit candidate list request model
"""

from containers import Container
from pydantic import BaseModel, Field, validator
from core.error import NoDataException
from core.message import ERR_MESSAGE
from typing import Optional


container = Container()
candidate_list_repo = container.candidates_list_repository()


class EditCandidateListRequest(BaseModel):
  """
  Edit candidate list request model
  """
  id: str = Field(..., title="Id", min_length=1)
  note: Optional[str] = Field(None, title="Note", max_length=256)
  fullname: str = Field(..., title="Full name", min_length=1, max_length=50)
  birthday: str = Field(..., title="Birthday", regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  full_address: str = Field(..., title="Full address", min_length=1, max_length=256)
  telephone_no: Optional[str] = Field(..., title="Telephone number",  regex="^0(\\d{9,10})$|^$")
  position_id: Optional[str] = Field(None, title="Position id", min_length=1)
  recommender_id: Optional[str] = None
  team_id: Optional[str] = Field(None, title="Team id", min_length=1)
  status: Optional[int] = Field(..., title="Candidate status")
  file_size: Optional[str] = Field(None, title="File size")
  file_ext: Optional[str] = Field(None, title="File ext")
  file: Optional[str] = Field(None, title="File")
  email: str = Field(..., title="Email", max_length=256, regex=r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$")

  @validator("email")
  def check_email(cls, email, values):
    # Get candidate by email and id candidate
    user = candidate_list_repo.check_email(email, values["id"])

    # Candidate exit
    if not user:
      raise NoDataException(message=ERR_MESSAGE.MSG_0002)
    return email
