"""
List add mail candidates response model
"""

from typing import List, Optional
from pydantic import BaseModel

class AddMailItem(BaseModel):
  """
    Add mail item
  """
  id: int
  body: Optional[str] = None
  title: Optional[str] = None
  candidate_id: int
  status: Optional[str] = None

class AddMailCandidatesResponse(BaseModel):
  mails: Optional[List[AddMailItem]] = None
