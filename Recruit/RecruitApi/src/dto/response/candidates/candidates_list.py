"""
List candidates response model
"""

from typing import List, Optional
from pydantic import BaseModel

class RecommenderItem(BaseModel):
  """
    Recommender item
  """
  id: str
  fullname: str

class CandidatesItem(BaseModel):
  """
    Candidate item
  """
  id: int
  fullname: str
  position: Optional[str] = None
  team: Optional[str] = None
  email: Optional[str] = None
  telephone_no: Optional[str] = None
  recommender_name: Optional[str] = None
  office: Optional[str] = None
  application_date: Optional[str] = None
  previous_status: Optional[str] = None
  status: Optional[str] = None
  cv_file_path: Optional[str] = None
  gender: str

class CandidatesListResponse(BaseModel):
  item: Optional[List[CandidatesItem]] = None
  list_recommender: Optional[List[RecommenderItem]] = None
