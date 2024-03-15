"""
  Request of notify
"""

from typing import Optional
from pydantic import BaseModel

class SettingShopNotifyRequest(BaseModel):
  content: Optional[str] = None
