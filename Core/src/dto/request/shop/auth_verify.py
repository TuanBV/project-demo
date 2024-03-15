"""
AuthVerify model
"""

from pydantic import BaseModel

class AuthVerifyRequest(BaseModel):
  """
    Properties of Auth Verify
  """
  time_now: float
  time_remaining: float
  otp: str
