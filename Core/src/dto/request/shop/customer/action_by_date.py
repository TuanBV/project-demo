"""
Action by date model
"""

from pydantic import BaseModel

class ActionByDateRequest(BaseModel):
  start_date: str
  end_date: str
  month_filter: str
  type_calendar: int
