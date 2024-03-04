"""
Parameter edit request
"""
from typing import Optional
from pydantic import BaseModel, Field

class FileItem(BaseModel):
  file: str
  file_name: str
  file_ext: str
  file_size: str

class MailEditRequest(BaseModel):
  """
    Properties mail edit request
  """
  title: str = Field(..., title="Title")
  body: str = Field(..., title="Body")
  carbon_copy: Optional[list] = Field(None, title="Carbon copy")
  attach_file: Optional[FileItem|str]
