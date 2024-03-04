"""
List teams response model
"""

from typing import List
from pydantic import BaseModel


class TeamItem(BaseModel):
  id: int
  name: str


class ListTeamsResponse(BaseModel):
  item: List[TeamItem]
