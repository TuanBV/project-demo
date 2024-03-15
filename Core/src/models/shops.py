"""
Shops model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, DATE, VARCHAR, FLOAT, INTEGER
from helpers.kbn import IntEnum, PaymentPlan
from models.entity_base import EntityBase


class Shops(EntityBase):
  """
  Shops model
  """
  shop_no = Column(VARCHAR)
  corporate_name = Column(VARCHAR)
  telephone_no = Column(VARCHAR)
  avatar = Column(VARCHAR)
  first_name = Column(VARCHAR)
  last_name = Column(VARCHAR)
  first_name_kana = Column(VARCHAR)
  last_name_kana = Column(VARCHAR)
  zip_code = Column(VARCHAR)
  address1 = Column(VARCHAR)
  address2 = Column(VARCHAR)
  address3 = Column(VARCHAR)
  prefecture = Column(VARCHAR)
  start_using_date = Column(DATE)
  contract_start_date = Column(DATE)
  contract_end_date = Column(DATE)
  payment_plan_kbn = Column(IntEnum(PaymentPlan))
  first_payment = Column(FLOAT)
  monthly_payment = Column(FLOAT)
  url = Column(VARCHAR)
  note= Column(VARCHAR)
  payment_method_code = Column(TINYINT)
  campaign_start_date = Column(DATE)
  campaign_end_date = Column(DATE)
  campaign_point = Column(INTEGER)
  campaign_note = Column(VARCHAR)
  days_for_printing = Column(INTEGER)
  logo = Column(VARCHAR)
  name = Column(VARCHAR)
  slogan = Column(VARCHAR)
  color = Column(VARCHAR)
  services_content = Column(VARCHAR)
  point_default = Column(INTEGER)
