"""
Admin model
"""
from typing import List
from pydantic import BaseModel


class AdminData(BaseModel):
  first_name: str
  first_name_kana: str
  avatar: str
  role_kbn: int
  id: int
  email: str
  last_name: str
  last_name_kana: str
  shop_notify_id: int

class ActionType(BaseModel):
  icon: str
  name: str
  color: str

class AdminLoginResponse(BaseModel):
  user: AdminData
  action_type: List[ActionType]
  role: int
