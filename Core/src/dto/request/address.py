"""
Address request models
"""
from __future__ import annotations
from pydantic import BaseModel, Field

class AddressRequest(BaseModel):
  prefecture: str
  address1: str = Field(min_length=1, max_length=100)
  address2: str = Field(min_length=1, max_length=100)
  address3: str = Field(max_length=100)
