"""
  Return data when edit member
"""
from typing import Optional
from pydantic import BaseModel

class MemberEdit(BaseModel):
  """
    Response when eit member
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


class MemberEditResponse(BaseModel):
  role: int
  token: str
  user: MemberEdit
