"""
Allow otp model
"""
from pydantic import BaseModel

# Allow otp model
class AllowOtpResponse(BaseModel):
  auth_two_step: str
  auth_two_step_type: str
