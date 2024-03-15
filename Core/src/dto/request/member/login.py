"""
  Member login model
"""
from pydantic import BaseModel, Field

class MemberLoginRequest(BaseModel):
  email: str = Field(..., title="The email", min_length=1, max_length=256)
  password: str = Field(..., examples=["Test123@"], title="The password", min_length=8, max_length=64)
