"""
Assessment candidate request model
"""

from pydantic import BaseModel, Field


class AssessmentRequest(BaseModel):
  """
  Assessment candidate request model
  """
  comment: str = Field(None, title="Comment")
  evaluate: str = Field(..., title="Evaluate", pattern="^[0-2]{1}$")
  id: str = Field(..., title="Interview detail id")


class AdminEvaluateRequest(BaseModel):
  """
  Admin evaluate candidate request model
  """
  evaluate: bool
