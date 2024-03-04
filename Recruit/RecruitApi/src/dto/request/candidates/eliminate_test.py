"""
Eliminate test request model
"""

from pydantic import BaseModel


class EliminateTestRequest(BaseModel):
  """
  Eliminate test request model
  """
  flag_not_test: bool
