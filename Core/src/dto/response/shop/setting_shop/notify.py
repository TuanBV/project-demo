"""
  Response of notify
"""

from typing import Optional
from pydantic import BaseModel

class SettingShopNotifyResponse(BaseModel):
  content: Optional[str] = None
