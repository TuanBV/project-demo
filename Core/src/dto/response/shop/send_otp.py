"""
Send otp model
"""
from pydantic import BaseModel

# Send otp model
class SendOtpResponse(BaseModel):
  message: str
  otp_token: str
  time_now: int
  time_remaining: int
