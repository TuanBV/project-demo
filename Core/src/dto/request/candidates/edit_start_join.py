"""
Edit start join candidate request model
"""
from pydantic import BaseModel, Field


class EditStartJoinCandidateRequest(BaseModel):
  """
  Edit start join candidate request model
  """
  start_join_date: str = Field(..., title="Start join date", pattern=r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12]\d|3[01])$")
