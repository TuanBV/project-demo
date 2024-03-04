"""
Edit mail offices request model
"""
from pydantic import BaseModel, Field
from helpers.const import REGEX_EMAIL

class EditMailOfficesRequest(BaseModel):
  """
  Edit mail offices request model
  """
  mail: str = Field(..., title="Mail", min_length=1, regex=REGEX_EMAIL)
  password: str = Field(..., title="Password mail")
  office: str = Field(..., title="Id van phong lam viec")

