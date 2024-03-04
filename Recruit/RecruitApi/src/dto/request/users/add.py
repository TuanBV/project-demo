"""
User register request
"""
from containers import Container
from pydantic import BaseModel, Field, validator
from core.error import NoDataException
from core.message import ERR_MESSAGE
from typing import Optional


container = Container()
user_repo = container.users_repository()

class UserRegisterRequest(BaseModel):
  """
    Properties User register request
  """
  employee_code: str = Field(..., title="Employee code", max_length=6)
  fullname: str = Field(..., title="Full name", min_length=1, max_length=50)
  email: str = Field(..., title="Email", regex="^[\\w.!#$%&’*+\\/=?^`{|}-]+@([\\w-]+\\.)+[\\w-]{2,}$", min_length=1, max_length=256)
  birthday: str = Field(..., title="Birth day", regex="^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$", min_length=1)
  registered_date: Optional[str] = Field(None, title="Register date", regex="^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$")
  full_address: str = Field(..., title="Full address", min_length=1, max_length=256)
  place_issued_identification: str = Field(..., title="Place issued identification", min_length=1, max_length=100)
  identification_number: str = Field(..., title="Identification number", min_length=1, max_length=12)
  date_issued_identification: str = Field(..., title="Date issued identification", regex="^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$")
  telephone_no: Optional[str] = Field(None, title="Telephone number", regex="^0(\\d{9,10})$|^$")
  position_id: Optional[int] = Field(None, title="Id position")
  office_id: Optional[int] = Field(None, title="Id office")
  gender: Optional[int] = Field(None, title="Gender")

  @validator("employee_code")
  def check_employee_code(cls, employee_code):
    # Get user by employee code
    user = user_repo.check_employee_code(employee_code)

    # Employee code exit
    if not user:
      raise NoDataException(message=ERR_MESSAGE.MSG_0001)
    return employee_code

  @validator("email")
  def check_email(cls, email):
    # Get user by employee code
    user = user_repo.check_email(email)

    # Employee code exit
    if not user:
      raise NoDataException(message=ERR_MESSAGE.MSG_0002)
    return email

  @validator("identification_number")
  def check_identification_number(cls, identification_number):
    # Get user by employee code
    user = user_repo.check_identification_number(identification_number)

    # Employee code exit
    if not user:
      raise NoDataException(message=ERR_MESSAGE.MSG_0003)
    return identification_number
