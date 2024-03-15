"""
  Response of notify
"""

from pydantic import BaseModel

class MemberNotifyResponse(BaseModel):
  content: str
  kbn: int
