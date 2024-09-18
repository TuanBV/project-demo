"""
Meeting rooms response
"""

from pydantic import BaseModel
from typing import List, Optional

class ItemRoom(BaseModel):
  """
    Response of meeting room
  """
  id: int
  name: str
  office_id: int

class ListMeetingRoomsResponse(BaseModel):
  item: Optional[List[ItemRoom]]= None

