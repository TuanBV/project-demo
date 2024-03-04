"""
Forgot password model
"""

from pydantic import BaseModel, Field
from helpers.const import REGEX_EMAIL

class ForgotPasswordRequest(BaseModel):
  """
    Properties
  """
  email: str = Field(..., title="Email", max_length=256, regex=REGEX_EMAIL)

