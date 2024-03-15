"""
Shop notify response
"""
from pydantic import BaseModel

class ShopNotifyResponse(BaseModel):
  content: str
