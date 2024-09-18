"""
Login model
"""

from pydantic import BaseModel, Field
from helpers.const import REGEX_EMAIL

# Login model
class UsersLoginRequest(BaseModel):
  """
    Properties
  """
  email: str = Field(..., title="Email", max_length=256, pattern=REGEX_EMAIL)
  password: str = Field(..., title="Password")
