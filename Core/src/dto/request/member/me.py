"""
  Member user model
"""
from pydantic import BaseModel
from dto.response.shop import DataAddress

class MemberUser(BaseModel):
  """
    Data member
  """
  address: DataAddress
  avatar_image: str
  customer_id: str
  customer_no: str
  first_name: str
  first_name_kana: str
  last_name: str
  last_name_kana: str
  mail_address: str
  member_register_date: str
  sex_type: str
  shop_name: str
  shop_no:  str
  telephone_no: str
  zip_code: str

class Member(BaseModel):
  role: int
  token: str
  user: MemberUser
