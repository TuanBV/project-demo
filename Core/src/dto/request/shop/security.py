"""
Security model
"""
from pydantic import BaseModel
from typing import Optional

# Security model
class SecurityRequest(BaseModel):
  two_fa_flg: int
  two_fa_kbn: int
  login_notification_flg: int
  password_change_notification_flg: int
  otp: Optional[str] = ""
