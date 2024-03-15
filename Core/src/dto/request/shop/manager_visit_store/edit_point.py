"""
Edit point model
"""

from pydantic import BaseModel, Field

# Edit point histories model
class EditPointHistoriesRequest(BaseModel):
  """
  Properties
  """
  changed_date: str = Field(..., title="The changed date")
  description: str = Field(None, title="The description", max_length=100)
  note: str = Field(None, title="The note", max_length=100)
  payment: str = Field(..., title="The amount", regex="^(([0-9](\\d{1,6}))|[\\d]{1})$", max_length=7)
  points: str = Field(..., title="The points", regex="^-?[0-9](\\d{0,6})$", min_length=1, max_length=8)

