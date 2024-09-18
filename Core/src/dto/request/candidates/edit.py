"""
Edit candidate request model
"""

from typing import Optional
from pydantic import BaseModel, Field


class FileItem(BaseModel):
  file: str
  file_ext: str
  file_size: str


class EditCandidateRequest(BaseModel):
  """
  Edit candidate request model
  """
  fullname: str = Field(..., title="Full name", min_length=1, max_length=50)
  email: str = Field(..., title="Email", max_length=256, pattern=r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$")
  birthday: str = Field(..., title="Birthday", pattern=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  full_address: str = Field(..., title="Full address", min_length=1, max_length=256)
  place_issued_identification: str = Field(..., title="Place issued identification", min_length=1, max_length=100)
  identification_number: str = Field(..., title="Identification number", max_length=12, pattern=r"^[0-9]{12}$")
  date_issued_identification: str = Field(..., title="Date issued identification", pattern=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  telephone_no: Optional[str] = Field(None, title="Telephone number", pattern=r"^0(\d{10,11})$|^$")
  position_id: Optional[str] = Field(None, title="Position id", pattern=r"^\d$", min_length=1)
  team_id: Optional[str] = Field(None, title="Team id", pattern=r"^\d$", min_length=1)
  cv_file: Optional[FileItem]
  office_id: Optional[str] = Field(None, title="Office id", pattern=r"^\d$", min_length=1)
  recommender_id: Optional[str] = Field(None, title="Recommender id", pattern=r"^\d$", min_length=1)
  status: Optional[str] = Field(None, title="Candidate status", pattern=r"^\d$")
