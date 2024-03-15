"""
  Member sign up temp model
"""

from pydantic import BaseModel, Field

class MemberSignUpTempRequest(BaseModel):
  email: str= Field(..., title="Mail Address", regex=r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$",
    min_length=1, max_length=256)
