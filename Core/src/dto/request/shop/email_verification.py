"""
Mail reset password model
"""
from containers import Container
from core.error import CrmException
from core.message import ERR_MESSAGE
from pydantic import BaseModel, Field, validator

container = Container()
shop_repository = container.shop_repository()

# Mail reset password model
class EmailVerificationRequest(BaseModel):
  """
    Properties
  """
  email: str = Field(..., title="Email", max_length=256, regex=r"^[\w.!#$%&’*+\/=?^`{|}-]+@([\w-]+\.)+[\w-]{2,}$")

  @validator("email")
  def shop_exist(cls, email):
    flag_check = shop_repository.check_email_exist(email)

    # Check flag to raise error
    if not flag_check:
      raise CrmException(message=ERR_MESSAGE.ERRMSG0040)

    return email
