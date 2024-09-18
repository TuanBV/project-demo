"""
Candidate item response model
"""

from typing import Optional
from pydantic import BaseModel
from helpers.kbn import (CandidateStatus)


class CandidateItemResponse(BaseModel):
  """
    Candidate item model
  """
  id: int
  fullname: str
  email: str
  full_address: str
  place_of_birth = str
  telephone_no: str
  application_date: str
  position_id: int
  team_id: int
  cv_file_path: str
  recommender_id: Optional[int] = None
  status: CandidateStatus
  previous_status: Optional[CandidateStatus] = None
  office: str
  gender: str


class CandidateConfirmResponse(BaseModel):
  """
    Confirm candidate item model
  """
  id: int
  fullname: str
  team: Optional[str] = None
  position: Optional[str] = None
  email: str
  full_address: Optional[str] = None
  telephone_no: Optional[str] = None
  birthday: Optional[str] = None
  school: Optional[str] = None
  place_issued_identification: Optional[str] = None
  identification_number: Optional[str] = None
  date_issued_identification: Optional[str] = None
  start_join_date: Optional[str] = None
  class_room: Optional[str] = None
  bank_account: Optional[str] = None
  bank_branch: Optional[str] = None
  vehicle_number: Optional[str] = None
  department: Optional[str] = None
  place_of_birth: Optional[str] = None
