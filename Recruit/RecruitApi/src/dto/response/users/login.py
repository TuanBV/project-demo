"""
User login model
"""

from pydantic import BaseModel


class UsersLoginResponse(BaseModel):
  employee_code: str
  email: str
  fullname: str
  position_id: int
  office_id: int
