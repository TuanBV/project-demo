"""
  Member check url model
"""

from pydantic import BaseModel

class CheckUrlRequest(BaseModel):
  url: str
