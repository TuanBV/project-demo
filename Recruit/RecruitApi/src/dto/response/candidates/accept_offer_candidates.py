"""
Accept Offer candidates response model
"""

from typing import List, Optional
from pydantic import BaseModel
from setting import settings

class AcceptOfferCandidate(BaseModel):
  """
    Accept offer candidate model
  """
  id: int
  fullname: str
  email: str
  telephone_no: str
  team_id: int
  team: str
  position_id: int
  position: str
  office: str
  status: str
  cv_file_path: str
  start_join_date: Optional[str] = None
  gender: str
  mail_id: Optional[int] = None
  title: Optional[str] = None
  body: Optional[str] = None
  carbon_copy: Optional[List]
  attached_file: Optional[str] = None
  attached_file_name: Optional[str] = None

  def __init__(self, **data) -> None:
    """Change cv file path"""
    data["cv_file_path"] = f'{settings.DOMAIN_FILE}/{data["cv_file_path"]}'
    super().__init__(**data)


class AcceptOfferCandidateResponse(BaseModel):
  """
    List accept offer candidate model
  """
  candidates: List[AcceptOfferCandidate]
