"""
Login model
"""

from pydantic import BaseModel, Field

# Login model
class ShopLoginRequest(BaseModel):
  """
    Properties
  """
  password: str = Field(..., title="Password", min_length=8, max_length=64)
  email: str = Field(..., title="Email", max_length=256, regex=r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$")
