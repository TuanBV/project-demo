"""
Edit action request model
"""

from typing import List, Optional
from pydantic import BaseModel

class PdfItem(BaseModel):
  pdf_file: str
  pdf_ext: str
  pdf_size: str

class ActionBody(BaseModel):
  action_note: Optional[str] = None
  list_pdf: Optional[List[PdfItem]] = None
  body: Optional[str] = None
  title: Optional[str] = None

class ActionType(BaseModel):
  id: int
  name: str
  color: str

class EditActionRequest(BaseModel):
  action_body: ActionBody
  action_type: ActionType
  template_id: Optional[int] = None
