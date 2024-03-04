"""
Candidate request model
"""

from typing import List
from pydantic import BaseModel


class CandidateItem(BaseModel):
  id: int
  score: str
  interview_id: int


class CandidateScoreRequest(BaseModel):
  """
  Send candidates mail request model
  """
  list_candidate: List[CandidateItem]
