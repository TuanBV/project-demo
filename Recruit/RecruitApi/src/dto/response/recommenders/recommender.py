"""
Recommender item response model
"""

from pydantic import BaseModel


class RecommenderItemResponse(BaseModel):
  """
    Recommender item model
  """
  id: str
  fullname: str
  email: str
  birthday: str
  full_address: str
  place_issued_identification: str
  identification_number: str
  date_issued_identification: str
  telephone_no: str
