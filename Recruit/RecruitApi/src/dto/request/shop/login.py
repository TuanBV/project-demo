"""
Login model
"""

from pydantic import BaseModel, Field

# Login model
class ShopLoginRequest(BaseModel):
  """
    Properties
  """
  mail: str = Field(..., title="Email")
  password: str = Field(..., title="Password")
