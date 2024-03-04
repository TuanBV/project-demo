"""
Parameter edit request
"""
from pydantic import BaseModel, Field

class ParameterEditRequest(BaseModel):
  """
    Properties parameter edit request
  """
  name: str = Field(..., title="Name parameter")
  table: str = Field(..., title="Name table")
  column: str = Field(..., title="Name column")
  note: str = Field(..., title="Note")
