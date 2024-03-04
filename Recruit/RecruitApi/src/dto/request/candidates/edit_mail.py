"""
Edit mail candidate request model
"""

from typing import Optional, List
from pydantic import BaseModel


class EditMailCandidate(BaseModel):
  """
  Edit mail candidate request model
  """
  title: Optional[str] = None
  list_email_cc: Optional[List[str]] = None
  body: Optional[str] = None
  candidate_email: Optional[str] = None
  candidate_id: Optional[int] = None
  id: Optional[int] = None
