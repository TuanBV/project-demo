"""
Position repository
"""

from core import CommonRepository
from models import Positions
from helpers import kbn

class PositionsRepository(CommonRepository):
  """
  Repository of Service position
  """


  # Get list position
  # Params: None
  # Output:
  #  return: List position
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      data_position = session.query(Positions).filter(Positions.is_deleted == kbn.DeleteFlag.OFF.value).all()

      payload["item"] = data_position

      return payload


  # Get position by id
  # Params:
  #   @position_id: Id position
  # Output:
  #   return: Data position
  def get_position_by_id(self, position_id):
    with self.session_factory_read() as session:
      return session.query(Positions).filter(Positions.id == position_id, Positions.is_deleted == kbn.DeleteFlag.OFF.value).first()
