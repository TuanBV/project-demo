"""
Login model
"""
from pydantic import BaseModel, Field

# Login model
class AdminLoginRequest(BaseModel):
  email: str = Field(..., title="Email", max_length=256)
  password: str = Field(..., title="Password", min_length=8, max_length=64)
