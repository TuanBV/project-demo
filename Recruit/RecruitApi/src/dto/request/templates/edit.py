"""
Template edit request
"""
from pydantic import BaseModel, Field

class TemplateEditRequest(BaseModel):
  """
    Properties template edit request
  """
  title: str = Field(..., title="Title template mail")
  body: str = Field(..., title="Content body of mail")
  note: str = Field(..., title="Note")
