"""
Shop account model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME
from helpers.kbn import (IntEnum, LoginNotifyFlg,
  PwChangedNotifyFlg, TwoFaFlg, TwoFaType, UserRole)
from models.entity_base import EntityBase


class ShopAccounts(EntityBase):
  """
  Shop account model
  """
  email = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  telephone_no = Column(VARCHAR)
  password = Column(VARCHAR)
  role_kbn = Column(IntEnum(UserRole))
  token = Column(VARCHAR)
  token_expiration_time = Column(DATETIME)
  last_changed_password_time = Column(DATETIME)
  password_change_notification_flg = Column(IntEnum(PwChangedNotifyFlg))
  login_notification_flg = Column(IntEnum(LoginNotifyFlg))
  two_fa_flg = Column(IntEnum(TwoFaFlg))
  two_fa_kbn = Column(IntEnum(TwoFaType))
  secret_otp = Column(VARCHAR)
  otp = Column(VARCHAR)
  otp_token = Column(VARCHAR)
