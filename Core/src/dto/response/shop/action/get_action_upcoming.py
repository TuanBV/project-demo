"""
Get action upcoming response
"""

from pydantic import BaseModel

class GetActionUpcomingResponse(BaseModel):
  """
  Action item model
  """
  name: str
  delivery_time: str
