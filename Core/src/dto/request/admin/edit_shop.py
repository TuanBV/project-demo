"""
Edit shop request model
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, validator
from core.error import CrmException
from core.message import ERR_MESSAGE
from helpers.kbn import (LoginNotifyFlg, PaymentMethod,
  PaymentPlan, PwChangedNotifyFlg, TwoFaFlg, TwoFaType, UserRole)


class Shop(BaseModel):
  """
  Shop model
  """
  avatar: Optional[str] = None
  avatar_image_ext: Optional[str] = None
  avatar_image_size: Optional[str] = None
  corporate_name: str = Field(..., title="Corporate name", min_length=1, max_length=50)
  telephone_no: str = Field(..., title="Telephone number", regex=r"^0(\d{9,10})$|^$")
  first_name: Optional[str] = Field(..., title="First Name", min_length=1, max_length=20)
  last_name: Optional[str] = Field(..., title="Last Name", min_length=1, max_length=20)
  first_name_kana: Optional[str] = Field(..., title="First Name Katakana", max_length=20, regex=r"^([ァ-ヴ]|ー)+$")
  last_name_kana: Optional[str] = Field(..., title="Last Name Katakana", max_length=20, regex=r"^([ァ-ヴ]|ー)+$")
  zip_code: Optional[str] = None
  address1: Optional[str] = None
  address2: Optional[str] = None
  address3: Optional[str] = None
  prefecture: Optional[str] = None
  start_using_date: str = Field(...,title="Start using date",regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/(0[1-9]|[1-2][0-9]|3[0-1])$")
  contract_start_date: str = Field(None, title="Contract start date",regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/01$|^$")
  contract_end_date: str = Field(None, title="Contract end date",regex=r"^(\d{4})\/(0[1-9]|1[0-2])\/01$|^$")

  @validator("contract_end_date")
  # Contract end date must greater than contract start date
  def end_date_gt_start_date(cls, contract_end_date, values):
    if (values["contract_start_date"] and contract_end_date and contract_end_date < values["contract_start_date"]):
      raise CrmException(message = ERR_MESSAGE.ERRMSG0046)
    return contract_end_date

  payment_plan_kbn: PaymentPlan = Field(title="Payment plan")
  first_payment: str = Field(None, title="First payment", regex=r"^(([1-9](\d{1,6}))|[\d]{1})$|^$")
  monthly_payment: str = Field(None, title="Monthly payment", regex=r"^(([1-9](\d{1,6}))|[\d]{1})$|^$")
  url: str = Field(..., title="Url shop", regex=r"^[^/]*$", min_length=1, max_length=50)
  note: str = Field(None, title="Note", max_length=400)
  payment_method_code: PaymentMethod = Field(title="Payment method")
  days_for_printing: str = Field(..., title="Time print confirm", regex=r"^[0-9]{1,4}$", max_length=4)
  services_content: str = Field(None, title="Services content", max_length=400)

class Account(BaseModel):
  """
  Account model
  """
  id: int = Field(None, title="Id account")
  password: str = Field(title="Password", max_length=64,
    regex=r"(?=.{8,})((?=.*\d)(?=.*[a-z])(?=.*[A-Z])|(?=.*\d)(?=.*[a-zA-Z])(?=.*[\W_])|(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])).*|^$")

  @validator("password")
  def password_must_be_english_character(cls, password):
    pattern = r"^[~`!@#$%^&*()_+=\[\]\\{}|;':\",./<>?a-zA-Z0-9-]+$"

    # Check password not empty and validate password by pattern
    if password and not re.search(pattern, password):
      raise CrmException(message=ERR_MESSAGE.ERRMSG0122)

    return password

  telephone_no: str = Field(title="Telephone number", regex=r"^0(\d{9,10})$|^$")
  password_change_notification_flg: PwChangedNotifyFlg = Field(..., title="Password changed notify flag")
  login_notification_flg: LoginNotifyFlg = Field(..., title="Login notify flag")
  two_fa_flg: TwoFaFlg = Field(..., title="Auth two step flag")
  two_fa_kbn: TwoFaType = Field(..., title="Auth two step type")
  role_kbn: UserRole = Field(..., title="Role account")
  email: str = Field(title="Email", max_length=256, regex=r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$|^$")

  @validator("email")
  def check_data_shop_account(cls, email, values):
    # Email empty but password or telephone not empty will
    # raise Error
    if (email == "" and (values["password"] != "" or values["telephone_no"] != "")):
      raise CrmException(message = ERR_MESSAGE.ERRMSG0184)
    # Email not empty
    elif email != "":
      # Telephone empty will raise Error
      if values["telephone_no"] == "":
        raise CrmException(message = ERR_MESSAGE.ERRMSG0184)

      # Check id in data manager or staff and password is empty
      # wil raise Error
      if "id" not in values and values["password"] == "":
        raise CrmException(message = ERR_MESSAGE.ERRMSG0184)

    return email

class EditShopRequest(BaseModel):
  """
  Edit shop request model
  """
  shop: Shop
  manager: Optional[Account] = None
  staff: Optional[Account] = None
  owner: Account

  @validator("owner")
  def email_not_duplicated(cls, owner, values):
    if values["manager"] and values["staff"]:
      if (values["manager"].email and values["staff"].email and (owner.email == values["manager"].email
          or values["manager"].email == values["staff"].email or values["staff"].email == owner.email)):
        raise CrmException(message=ERR_MESSAGE.ERRMSG0047)

    # Check 2 email not duplicate (owner, staff)
    elif not values["manager"] and values["staff"] and values["staff"].email:
      if owner.email == values["staff"].email:
        raise CrmException(message=ERR_MESSAGE.ERRMSG0047)

    # Check 2 email not duplicate (owner, manager)
    elif values["manager"] and not values["staff"]  and values["manager"].email:
      if owner.email == values["manager"].email:
        raise CrmException(message=ERR_MESSAGE.ERRMSG0047)

    return owner
