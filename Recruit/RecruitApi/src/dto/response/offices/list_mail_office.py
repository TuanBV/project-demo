"""
Mail Offices response
"""

from pydantic import BaseModel
from typing import List, Optional

class MailOffice(BaseModel):
  """
    Response of mail office
  """
  id: int
  mail_admin: str

class ListMailOfficeResponse(BaseModel):
  offices: Optional[List[MailOffice]]= None
