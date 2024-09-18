"""
Edit candidate request model
"""

from pydantic import BaseModel, Field


class CandidatesIdRequest(BaseModel):
  """
  Send candidates mail request model
  """
  candidates_id: list = Field(..., title="Candidates id")
