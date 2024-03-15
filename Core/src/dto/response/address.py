"""
Address response models
"""
from __future__ import annotations
from typing import List
from pydantic import BaseModel

class AddressItem(BaseModel):
  prefecture: str
  district: str
  address: str
  zip_code: str

class AddressResponse(BaseModel):
  total_record: int
  item: List[AddressItem]
