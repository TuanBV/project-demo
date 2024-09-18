"""
Shop login model
"""

from pydantic import BaseModel

class ShopLoginResponse(BaseModel):
  status: str
  shopcode: str
  mail: str
  name: str
  campaign_code: str
  shop_type: int
