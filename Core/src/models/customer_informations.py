"""
Customers model
"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, FLOAT
from models.entity_base import EntityBase


class CustomerInformations(EntityBase):
  """
  Customers model
  """
  customer_no = Column(VARCHAR)
  shop_no = Column(VARCHAR)
  amount_1_month = Column(FLOAT, default=0.0)
  amount_3_month = Column(FLOAT, default=0.0)
  amount_6_month = Column(FLOAT, default=0.0)
  amount_12_month = Column(FLOAT, default=0.0)
  visited_1_month = Column(INTEGER, default=0)
  visited_3_month = Column(INTEGER, default=0)
  visited_6_month = Column(INTEGER, default=0)
  visited_12_month = Column(INTEGER, default=0)
  date_act_future = Column(INTEGER, default=0)
  date_act_sent_all = Column(INTEGER, default=0)
  date_act_sent_email = Column(INTEGER, default=0)
  date_act_sent_postcard = Column(INTEGER, default=0)
  date_act_sent_flyer = Column(INTEGER, default=0)
  date_visited = Column(INTEGER, default=0)
  date_registered = Column(INTEGER, default=0)
