"""
  Check Token
"""
from pydantic import BaseModel

class MemberTokenResponse(BaseModel):
  email: str
