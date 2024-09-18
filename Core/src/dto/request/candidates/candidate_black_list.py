"""
Edit candidate list request model
"""

from pydantic import BaseModel, Field
from typing import Optional

class CandidateBlackListRequest(BaseModel):
  """
  Edit candidate list request model
  """
  id: str = Field(..., title="Id")
  reason: Optional[str] = Field(title="Note", min_length=1)
