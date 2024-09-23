"""
User register request
"""
from containers import Container
from pydantic import BaseModel, Field, field_validator
from core.error import NoDataException
from core.message import ERR_MESSAGE
# from typing import Optional


container = Container()
user_repo = container.users_repository()
pattern_pw = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
class UserRegisterRequest(BaseModel):
  """
    Properties User register request
  """
  fullname: str = Field(..., title="Full name", min_length=1, max_length=50)
  username: str = Field(..., title="Username", pattern=r"^\S+$", min_length=5, max_length=50)
  email: str = Field(..., title="Email", pattern="^[\\w.!#$%&’*+\\/=?^`{|}-]+@([\\w-]+\\.)+[\\w-]{2,}$", min_length=1, max_length=256)
  role: str = Field(..., title="Role", max_length=1, min_length=1, pattern=r"^(1|2|3)$")
  # password: str = Field(..., title="Password", pattern=pattern_pw, min_length=8, max_length=64)

  # @field_validator("employee_code")
  # def check_employee_code(cls, employee_code):
  #   # Get user by employee code
  #   user = user_repo.check_employee_code(employee_code)

  #   # Employee code exit
  #   if not user:
  #     raise NoDataException(message=ERR_MESSAGE.MSG_0001)
  #   return employee_code

  # @field_validator("email")
  # def check_email(cls, email):
  #   # Get user by employee code
  #   user = user_repo.check_email(email)

  #   # Employee code exit
  #   if not user:
  #     raise NoDataException(message=ERR_MESSAGE.MSG_0002)
  #   return email

  # @field_validator("identification_number")
  # def check_identification_number(cls, identification_number):
  #   # Get user by employee code
  #   user = user_repo.check_identification_number(identification_number)

  #   # Employee code exit
  #   if not user:
  #     raise NoDataException(message=ERR_MESSAGE.MSG_0003)
  #   return identification_number
