"""
  Response when login success
"""

from typing import Optional
from pydantic import BaseModel

class DataMember(BaseModel):
  """
    Return data of member
  """
  address1: str
  address2: str
  address3: str
  avatar: str
  birthday: str
  id: str
  customer_no:str
  first_name: str
  first_name_kana: str
  last_name: str
  last_name_kana: str
  email: str
  sex_kbn: str
  shop_no: str
  telephone_no: Optional[str] = None
  zip_code: str
  shop_url: str

class MemberLoginResponse(BaseModel):
  role: int
  token: str
  user: DataMember
