"""
Add template response
"""

from typing import List, Optional
from pydantic import BaseModel


class AddTemplateResponse(BaseModel):
  template_id: int
  template_name: str
  pdf: Optional[List[str]] = None
