"""
Add point model
"""

from pydantic import BaseModel, Field

# Get customer model
class AddPointHistoriesRequest(BaseModel):
  """
  Properties
  """
  changed_date: str = Field(..., title="The changed date")
  payment: str = Field(..., title="The amount", regex="^(([0-9](\\d{1,6}))|[\\d]{1})$", max_length=7)
  points: str = Field(..., title="The points", regex="^-?[0-9](\\d{0,6})$", min_length=1, max_length=8)
  description: str = Field(None, title="The description", max_length=100)
  note: str = Field(None, title="The note", max_length=100)
  changed_points: float = Field(default=0.0)

