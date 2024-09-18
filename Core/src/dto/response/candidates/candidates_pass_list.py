"""
List candidates pass response model
"""

from typing import List, Optional
from pydantic import BaseModel

class CandidatesPassItem(BaseModel):
  """
    Candidate pass item
  """
  id: int
  fullname: str
  position: Optional[str] = None
  team: Optional[str] = None
  office: Optional[str] = None
  email: Optional[str] = None
  telephone_no: Optional[str] = None
  birthday: Optional[str] = None
  full_address: Optional[str] = None
  start_join_date: Optional[str] = None
  id_template: Optional[int] = None
  title: Optional[str] = None
  body: Optional[str] = None
  status: Optional[str] = None
  carbon_copy: Optional[List[str]] = None
  gender: str

class CandidatesPassListResponse(BaseModel):
  item: Optional[List[CandidatesPassItem]] = None
