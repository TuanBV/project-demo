""""
  Response of check url
"""

from pydantic import BaseModel

class CheckUrlResponse(BaseModel):
  color: str
  corporate_name: str
  logo: str
  name: str
  shop_no: str
  slogan: str
