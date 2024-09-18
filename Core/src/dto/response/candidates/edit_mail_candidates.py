"""
List add mail candidates response model
"""

from typing import List, Optional
from pydantic import BaseModel

class EditMailCandidatesResponse(BaseModel):
  """
    Add mail item
  """
  id: int
  body: Optional[str] = None
  title: Optional[str] = None
  candidate_id: int
  carbon_copy: Optional[List[str]] = None
