"""
Team repository
"""

from core import CommonRepository
from models import Teams
from helpers import kbn

class TeamsRepository(CommonRepository):
  """
  Repository of Service team
  """


  # Get list team
  # Params: None
  # Output:
  #  return: List team
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      data_team = session.query(Teams).filter(Teams.is_deleted == kbn.DeleteFlag.OFF.value).all()

      payload["item"] = data_team

      return payload


  # Get team by id
  # Params:
  #   @team_id: Id team
  # Output:
  #   return: Data team
  def get_team_by_id(self, team_id):
    with self.session_factory_read() as session:
      return session.query(Teams).filter(Teams.id == team_id, Teams.is_deleted == kbn.DeleteFlag.OFF.value).first()
