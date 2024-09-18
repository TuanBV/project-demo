"""
List leader response
"""

from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
  """
    Response of item user in list leader user
  """
  employee_code: str
  fullname: str

class ListLeaderResponse(BaseModel):
  item: Optional[List[User]]= None
