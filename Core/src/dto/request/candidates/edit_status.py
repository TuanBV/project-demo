"""
Edit status candidate request model
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from helpers.kbn import (CandidateStatus)


class EditStatusCandidateRequest(BaseModel):
  """
  Edit status candidate request model
  """
  list_id: Optional[List[int]]
  status: CandidateStatus = Field(..., title="Candidate status")
