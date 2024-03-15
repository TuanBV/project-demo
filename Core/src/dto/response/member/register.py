""""
  Response register member
"""

from pydantic import BaseModel

class DataRegisterMember(BaseModel):
  """"
    Return data when register member
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
  registered_date: str
  password: str
  sex_kbn: str
  shop_no: str
  telephone_no: str
  zip_code: str

class MemberRegisterResponse(BaseModel):
  role: int
  token: str
  user: DataRegisterMember
