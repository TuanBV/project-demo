"""
User response and list user response
"""

from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
  """
    Response of item user in list user
  """
  employee_code: str
  email: str
  fullname: str
  full_address: str
  telephone_no: Optional[str] = None
  office: Optional[str] = None
  position: Optional[str] = None
  gender: int


class ListUserResponse(BaseModel):
  list_user: Optional[List[User]]= None

class UserResponse(BaseModel):
  """
    Response of user
  """
  employee_code: str
  fullname: str
  email: str
  birthday: str
  full_address: str
  telephone_no: Optional[str] = None
  office_id: int
  registered_date: Optional[str] = None
  position_id: int
  gender: int
  place_issued_identification: Optional[str] = None
  identification_number: Optional[str] = None
  date_issued_identification: Optional[str] = None
