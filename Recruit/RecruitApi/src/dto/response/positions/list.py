"""
List positions response model
"""

from typing import List
from pydantic import BaseModel


class PositionItem(BaseModel):
  id: int
  name: str


class ListPositionsReponse(BaseModel):
  item: List[PositionItem]
