"""
  Response of check notify
"""

from typing import List
from pydantic import BaseModel

class ItemPayload(BaseModel):
  id: str
  kbn: int
  read_flg: int

class MemberCheckNotifyResponse(BaseModel):
  notifications: List[ItemPayload]
