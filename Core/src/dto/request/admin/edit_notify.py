"""
  Edit shop notify request
"""

from typing import Optional
from pydantic import BaseModel

class EditShopNotifyRequest(BaseModel):
  content: Optional[str] = None
