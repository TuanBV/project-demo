"""
Candidate item response model
"""

from typing import Optional
from pydantic import BaseModel

class FormCandidateResponse(BaseModel):
  """
    Candidate item model
  """
  fullname: str
  birthday: Optional[str] = None
  place_of_birth: Optional[str] = None
  full_address: Optional[str] = None
  identification_number: Optional[str] = None
  date_issued_identification: Optional[str] = None
  place_issued_identification: Optional[str] = None
  bank_account: Optional[str] = None
  bank_branch: Optional[str] = None
  vehicle_number: Optional[str] = None
  telephone_no: Optional[str] = None
  start_join_date: Optional[str] = None

