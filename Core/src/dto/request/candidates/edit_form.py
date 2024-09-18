"""
Edit form candidate request model
"""

from typing import Optional
from pydantic import BaseModel, Field


class EditFormCandidateRequest(BaseModel):
  """
  Edit form candidate request model
  """
  fullname: str = Field(..., title="Full name", min_length=1, max_length=50)
  birthday: str = Field(..., title="Birthday", pattern=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  place_of_birth: str = Field(..., title="Place of birth", min_length=1, max_length=256)
  full_address: str = Field(..., title="Full address", min_length=1, max_length=256)
  identification_number: str = Field(..., title="Identification number", max_length=12, pattern=r"^[0-9]{12}$")
  date_issued_identification: str = Field(..., title="Date issued identification", pattern=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  place_issued_identification: str = Field(..., title="Place issued identification", min_length=1, max_length=100)
  bank_account: Optional[str] | None = Field(None, title="Bank account")
  bank_branch: Optional[str] | None = Field(None, title="Bank branch")
  vehicle_number: Optional[str] | None = Field(None, title="Vehicle number")
  start_join_date: str = Field(None, title="Start join date", pattern=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  telephone_no: str = Field(None, title="Telephone number", pattern=r"^0(\d{9,10})$")
