"""
  Member register and edit model
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, validator

from core.error import CrmException
from core.message import ERR_MESSAGE
from helpers.common import age
from utils.date import format_date_time, get_current_time_obj

class MemberRegisterRequest(BaseModel):
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
  email: str = Field(..., title="Mail Address", regex=r"^[\w.!#$%&'*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$", min_length=1, max_length=256)
  birthday: str = Field(..., title="Birth day", regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)

  @validator("birthday")
  # Check birthday
  def check_birthday(cls, birthday):
    # Age is greater than 150 will return an error
    if int(age(birthday)) > 150:
      raise CrmException(message=ERR_MESSAGE.ERRMSG0024)

    # Birthday is greater than current time will return an error
    if birthday > format_date_time(get_current_time_obj(), "%Y/%m/%d %H:%M"):
      raise CrmException(message=ERR_MESSAGE.ERRMSG0044)

    return birthday

  sex_kbn: Optional[str] = Field(None, title="Sex", regex=r"^[0-3]{1}$|^$")
  zip_code: str = Field(..., title="Zipcode", regex=r"^[0-9]{7}$", min_length=1, max_length=7)
  address1: str = Field(..., title="Address 1", min_length=1, max_length=100)
  address2: str = Field(..., title="Address 2", min_length=1, max_length=100)
  address3:  Optional[str] = None
  prefecture: Optional[str] = None
  password: Optional[str] = Field(None, title="Password", min_length=8, max_length=64,
    regex=r"(?=.{8,})((?=.*\d)(?=.*[a-z])(?=.*[A-Z])|(?=.*\d)(?=.*[a-zA-Z])(?=.*[^A-Za-z0-9])|(?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])).*")

  @validator("password")
  def password_must_be_english_character(cls, password):
    pattern = r"^[~`!@#$%^&*()_+=\[\]\\{}|;':\",./<>?a-zA-Z0-9-]+$"
    # Check password not empty and validate password by pattern
    if password and not re.search(pattern, password):
      raise CrmException(message=ERR_MESSAGE.ERRMSG0122)

    return password


  customer_tmp_id: Optional[str] = None
