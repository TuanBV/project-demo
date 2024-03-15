"""
Security model
"""
from pydantic import BaseModel

# Login model
class SecurityResponse(BaseModel):
  two_fa_flg: int
  two_fa_kbn: int
  login_notification_flg: str
  password_change_notification_flg: str
