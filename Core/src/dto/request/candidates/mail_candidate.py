"""
Add mail candidate request model
"""

from typing import Optional, List
from pydantic import BaseModel


class MailCandidate(BaseModel):
  """
  Add mail candidate request model
  """
  list_id_candidate: Optional[List[int]]
