"""
Change password model
"""

from pydantic import BaseModel, Field
from helpers.const import REGEX_PASSWORD

class ChangePasswordRequest(BaseModel):
  """
    Properties
  """
  # password: str = Field(..., title="Password", max_length=64, pattern=REGEX_PASSWORD)
  password: str = Field(..., title="Password", max_length=64)
  # new_password: str = Field(..., title="Password", max_length=64, pattern=REGEX_PASSWORD)
  new_password: str = Field(..., title="Password", max_length=64)
  # confirm_password: str = Field(..., title="Confirm password", max_length=64, pattern=REGEX_PASSWORD)
  confirm_password: str = Field(..., title="Confirm password", max_length=64)

