"""
User login model
"""

from pydantic import BaseModel


class UsersLoginResponse(BaseModel):
  email: str
  fullname: str
  role: int
  username: str
