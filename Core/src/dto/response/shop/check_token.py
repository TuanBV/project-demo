"""
Check token model
"""
from pydantic import BaseModel, Field

# Check token model
class CheckTokenResponse(BaseModel):
  email: str = Field(..., title="Email", max_length=256)
