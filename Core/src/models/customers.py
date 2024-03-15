"""
Customers model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, DATE, INTEGER, FLOAT
from helpers.kbn import IntEnum, Rank, RankKBN, SexKBN, SubscriptionFlag, UserRole
from models.entity_base import EntityBase


class Customers(EntityBase):
  """
  Customers model
  """
  customer_no = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  avatar = Column(VARCHAR)
  first_name = Column(VARCHAR)
  last_name = Column(VARCHAR)
  first_name_kana = Column(VARCHAR)
  last_name_kana = Column(VARCHAR)
  telephone_no = Column(VARCHAR)
  email = Column(VARCHAR)
  birthday = Column(DATE)
  sex_kbn = Column(IntEnum(SexKBN), default=SexKBN.BLANK.value)
  zip_code = Column(VARCHAR)
  address1 = Column(VARCHAR)
  address2 = Column(VARCHAR)
  address3 = Column(VARCHAR)
  prefecture = Column(VARCHAR)
  note = Column(VARCHAR)
  points = Column(INTEGER, default=0)
  last_visited_date = Column(DATE)
  password = Column(VARCHAR)
  role_kbn = Column(IntEnum(UserRole), default=UserRole.CUSTOMER.value)
  token = Column(VARCHAR)
  token_expiration_time = Column(DATETIME)
  total_amount = Column(FLOAT, default=0.0)
  total_visits = Column(INTEGER,  default=0)
  subscription_flag = Column(IntEnum(SubscriptionFlag), default=SubscriptionFlag.YES.value)
  rank_kbn = Column(IntEnum(RankKBN), default=RankKBN.YES.value)
  rank = Column(IntEnum(Rank), default=Rank.BLANK.value)
  registered_date = Column(DATE)
