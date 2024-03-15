"""
  Member change status notify model
"""

from pydantic import BaseModel, Field

class MemberChangeStatusNotifyRequest(BaseModel):
  type: str = Field(..., title="Type of notify", regex=r"^[1-2]{1}$", min_length=1)
