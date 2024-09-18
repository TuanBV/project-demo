"""
Offer candidates response model
"""

from typing import List
from pydantic import BaseModel
from setting import settings

class OfferCandidate(BaseModel):
  """
    Offer candidate model
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
  gender: str

  def __init__(self, **data) -> None:
    """Change cv file path"""
    data["cv_file_path"] = f'{settings.DOMAIN_FILE}/{data["cv_file_path"]}'
    super().__init__(**data)


class OfferCandidateResponse(BaseModel):
  """
    List Offer candidate model
  """
  candidates: List[OfferCandidate]
