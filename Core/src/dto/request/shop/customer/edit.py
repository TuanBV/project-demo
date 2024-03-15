"""
Add customer model
"""

from containers import Container
from core.error import CrmException
from core.message import ERR_MESSAGE
from helpers import context
from helpers.common import age
from pydantic import BaseModel, Field, validator
from typing import Optional
from utils.date import get_current_time_obj

container = Container()
shop_repository = container.shop_repository()

class EditCustomerRequest(BaseModel):
  """
  Add customer request model
  """
  avatar: Optional[str] = None
  avatar_ext: Optional[str] = None
  avatar_size: Optional[str] = None

  first_name: str = Field(..., title="First Name", min_length=1, max_length=20)
  last_name: str = Field(..., title="Last Name", min_length=1, max_length=20)
  telephone_no: Optional[str] = Field(None, title="Telephone number", regex="^0(\\d{9,10})$|^$")
  first_name_kana: str = Field(..., title="First Name Katakana", regex="^([ァ-ヴ]|ー)+$", min_length=1, max_length=20)
  last_name_kana: str = Field(..., title="Last Name Katakana", regex="^([ァ-ヴ]|ー)+$", min_length=1, max_length=20)
  birthday: str = Field(..., title="Birth day", regex="^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  sex_kbn: Optional[str] = Field(None, title="Sex", regex="^[0-3]{1}$|^$")
  zip_code: str = Field(..., title="Zipcode", regex="^[0-9]{7}$", min_length=1, max_length=7)
  prefecture: str
  customer_no: Optional[str] = Field(None)
  address1: str = Field(min_length=1, max_length=100)
  address2: str = Field(min_length=1, max_length=100)
  address3: str = Field(max_length=100)
  password: str = Field(None, title="Password",
    regex="(?=.{8,})((?=.*\\d)(?=.*[a-z])(?=.*[A-Z])|(?=.*\\d)(?=.*[a-zA-Z])(?=.*[^A-Za-z0-9])|(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])).*", min_length=8, max_length=64)
  subscription_flag: Optional[str] = Field(None, title="Subscription flag", regex="^[0-1]{1}$")
  is_deleted: Optional[str] = Field(None, title="Delete Flag", regex="^[0-1]{1}$")
  rank: str = Field(..., title="Rank", regex="^[0-4]|[9]{1}$")
  registered_date: str = Field(..., title="Register Date", regex="^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  email: str = Field(..., title="Mail Address", regex="^[\\w.!#$%&’*+\\/=?^`{|}-]+@([\\w-]+\\.)+[\\w-]{2,}$", min_length=1, max_length=256)

  @validator("birthday")
  def check_age(cls, birthday):
    time_current = get_current_time_obj().strftime("%Y/%m/%d %H:%M:%S")
    # Check age > 150
    if int(age(birthday)) > 150:
      raise CrmException(message=ERR_MESSAGE.ERRMSG0024)

    # Birthday > time current
    if birthday > time_current:
      raise CrmException(message=ERR_MESSAGE.ERRMSG0025)

    return birthday

  @validator("email")
  def shop_exist(cls, email, values):
    # Get information from context
    shop = context.user.value

    # Get shop_no of shop
    shop_no = shop["user"]["shop_no"]
    flag_check = shop_repository.check_customer_exist(email, shop_no, values["customer_no"])

    # Check flag to raise error
    if not flag_check or not shop_no:
      raise CrmException(message=ERR_MESSAGE.ERRMSG0038)

    return email

