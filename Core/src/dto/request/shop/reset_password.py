"""
Reset password model
"""
from pydantic import BaseModel, Field, validator
from containers import Container
from core.error import CrmException
from core.message import ERR_MESSAGE

container = Container()
shop_repository = container.shop_repository()

# Reset password model
class ResetPasswordRequest(BaseModel):
  """
    Request body of reset password
  """
  password_new: str = Field(..., examples=["Test5678"], title="New password", min_length=8, max_length=64,
      regex="(?=.{8,})((?=.*\\d)(?=.*[a-z])(?=.*[A-Z])|(?=.*\\d)(?=.*[a-zA-Z])(?=.*[\\W_])|(?=.*[a-z])(?=.*[A-Z])(?=.*[\\W_])).*")
  confirm_password: str = Field(..., examples=["Test5678"], title="Confirm new password")

  @validator("confirm_password")
  def check_password(cls, confirm_password, values):
    flag_check = shop_repository.check_match_password(confirm_password, values["password_new"])

    # Check flag to raise error
    if not flag_check:
      raise CrmException(message=ERR_MESSAGE.ERRMSG0039)

    return confirm_password
