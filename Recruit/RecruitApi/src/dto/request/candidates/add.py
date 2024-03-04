"""
Add candidate request model
"""

from typing import Optional
from pydantic import BaseModel, Field
from helpers.const import REGEXP_NUMBER, REGEXP_DECIMAL


class FileItem(BaseModel):
  file: str
  file_ext: str
  file_size: str


class AddCandidateRequest(BaseModel):
  """
  Add candidate request model
  """
  fullname: str = Field(..., title="Full name", min_length=1, max_length=50)
  email: str = Field(..., title="Email", max_length=256, regex=r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$")
  birthday: str = Field(..., title="Birthday", regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  full_address: str = Field(..., title="Full address", min_length=1, max_length=256)
  telephone_no: Optional[str] = Field(..., title="Telephone number", regex=r"^0(\d{9,10})$|^$")
  position_id: Optional[str] = Field(..., title="Position id", regex=REGEXP_NUMBER, min_length=1)
  team_id: Optional[str] = Field(..., title="Team id", regex=REGEXP_NUMBER, min_length=1)
  cv_file: Optional[FileItem]
  recommender_id: Optional[str] = Field(None, title="Recommender id", regex=r"^\d+$|^$")
  office_id: Optional[str] = Field(..., title="Office id", regex=REGEXP_NUMBER, min_length=1)
  gender: Optional[str] = Field(..., title="Gender", regex=r"^(0|1|2)$", min_length=1)
  number_experiences: Optional[str] = Field(..., title="Number experience", regex=REGEXP_DECIMAL)
