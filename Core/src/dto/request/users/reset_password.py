"""
Reset password model
"""

from pydantic import BaseModel, Field
from helpers.const import REGEX_PASSWORD

class ResetPasswordRequest(BaseModel):
  """
    Properties
  """
  # new_password: str = Field(..., title="New password", max_length=64, pattern=REGEX_PASSWORD)
  new_password: str = Field(..., title="New password", max_length=64)
  # confirm_password: str = Field(..., title="Confirm password", max_length=64, pattern=REGEX_PASSWORD)
  confirm_password: str = Field(..., title="Confirm password", max_length=64)
