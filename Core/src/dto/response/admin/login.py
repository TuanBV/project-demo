"""
Admin model
"""
from typing import List
from pydantic import BaseModel


class AdminData(BaseModel):
  id: int
  username: str
  email: str
  role_kbn: int

class AdminLoginResponse(BaseModel):
  user: AdminData
  role: int
