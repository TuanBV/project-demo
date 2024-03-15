"""
Check token model
"""
from containers import Container
from core.error import CrmUnauthorizedException
from core.message import ERR_MESSAGE
from pydantic import BaseModel, validator

container = Container()
shop_repository = container.shop_repository()

# Check token model
class CheckTokenRequest(BaseModel):
  """
    Properties and validator
  """
  token: str

  @validator("token")
  def verify_token(cls, token):
    flag_check = shop_repository.verify_token(token)

    # Check flag to raise error
    if not flag_check:
      CrmUnauthorizedException(message=ERR_MESSAGE.ERRMSG0042)

    return token

