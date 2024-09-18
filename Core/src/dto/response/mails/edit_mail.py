"""
Edit mail response model
"""

from typing import Optional
from pydantic import BaseModel, Field
from setting import settings

class EditMailResponse(BaseModel):
  """
    Edit mail model
  """
  title: str = Field(..., title="Title")
  body: str = Field(..., title="Body")
  carbon_copy: Optional[list] = Field(None, title="Carbon copy")
  attached_file: Optional[str] | None = Field(None, title="Attach file")
  attached_file_name: Optional[str] | None = Field(None, title="Attach file name")

  def __init__(self, **data) -> None:
    """Change attach file"""

    if "attached_file" in data and data["attached_file"]:
      data["attached_file"] = f'{settings.DOMAIN_FILE}/{data["attached_file"]}'
    super().__init__(**data)
