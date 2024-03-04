"""
Edit recommender request model
"""

from typing import Optional
from pydantic import BaseModel, Field
from helpers.const import REGEX_TELEPHONE_NO

class EditRecommenderRequest(BaseModel):
  """
  Edit recommender request model
  """
  fullname: str = Field(..., title="Full name", min_length=1, max_length=50)
  email: str = Field(..., title="Email", max_length=256, regex=r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$")
  birthday: str = Field(..., title="Birthday", regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  full_address: str = Field(..., title="Full address", min_length=1, max_length=256)
  place_issued_identification: str = Field(..., title="Place issued identification", min_length=1, max_length=100)
  identification_number: str = Field(..., title="Identification number", max_length=12, regex=r"^[0-9]{12}$")
  date_issued_identification: str = Field(..., title="Date issued identification", regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  telephone_no: Optional[str] = Field(None, title="Telephone number", regex=REGEX_TELEPHONE_NO)
