"""
  Member change password model
"""
import re
from pydantic import BaseModel, Field, validator
from containers import Container
from core.error import CrmException
from core.message import ERR_MESSAGE

container = Container()
shop_repository = container.shop_repository()

class MemberChangePasswordRequest(BaseModel):
  """
    Member change password request model
  """
  password: str = Field(..., title="Password", min_length=1 ,max_length=64,
    regex=r"(?=.{8,})((?=.*\d)(?=.*[a-z])(?=.*[A-Z])|(?=.*\d)(?=.*[a-zA-Z])(?=.*[\W_])|(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])).*",)

  @validator("password")
  def password_must_be_english_character(cls, password):
    pattern = r"^[~`!@#$%^&*()_+=\[\]\\{}|;':\",./<>?a-zA-Z0-9-]+$"
    # Check password not empty and validate password by pattern
    if password and not re.search(pattern, password):
      raise CrmException(message=ERR_MESSAGE.ERRMSG0122)

    return password

  confirm_password: str = Field(..., examples=["Test123@"], title="The confirm password", min_length=8, max_length=64)

  @validator("confirm_password")
  def check_password(cls, confirm_password, values):
    flag_check = shop_repository.check_match_password(confirm_password, values["password"])
    # Check flag to raise error
    if not flag_check:
      raise CrmException(message=ERR_MESSAGE.ERRMSG0039)
    return confirm_password
