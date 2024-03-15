"""
  Member register and edit model
"""

from typing import Optional
from pydantic import BaseModel, Field

class MemberDeleteRequest(BaseModel):
  is_deleted: int


class MemberEditRequest(BaseModel):
  """
      Register and edit member
  """
  avatar: Optional[str] = None
  avatar_ext: Optional[str] = None
  avatar_size: Optional[str] = None
  first_name: str = Field(..., title="First Name", min_length=1, max_length=20)
  last_name: str = Field(..., title="Last Name", min_length=1, max_length=20)
  telephone_no: Optional[str] = Field(None, title="Telephone number", regex=r"^0(\d{9,10})$|^$")
  first_name_kana: str = Field(..., title="First Name Katakana", regex=r"^([ァ-ヴ]|ー)+$", min_length=1, max_length=20)
  last_name_kana: str = Field(..., title="Last Name Katakana", regex=r"^([ァ-ヴ]|ー)+$", min_length=1, max_length=20)
  birthday: str  = Field(..., title="Birth day", regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$",min_length=1)
  sex_kbn: Optional[str] = Field(None, title="Sex", regex=r"^[0-3]{1}$|^$")
  zip_code: str = Field(..., title="Zipcode", regex=r"^[0-9]{7}$", min_length=1, max_length=7)
  address1: str = Field(..., title="Address 1", min_length=1, max_length=100)
  address2: str = Field(..., title="Address 2", min_length=1, max_length=100)
  address3:  Optional[str] = None
  password: str = Field(None, title="Password",
    regex="(?=.{8,})((?=.*\\d)(?=.*[a-z])(?=.*[A-Z])|(?=.*\\d)(?=.*[a-zA-Z])(?=.*[^A-Za-z0-9])|(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])).*", min_length=8, max_length=64)
