"""
Notify model
"""
from pydantic import BaseModel

class CheckNotifyResponse(BaseModel):
  read_flg: int

class NotifyResponse(BaseModel):
  content: str
