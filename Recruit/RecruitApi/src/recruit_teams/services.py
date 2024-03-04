"""
Teams Service
"""

from recruit_teams import TeamsRepository
from fastapi.encoders import jsonable_encoder


class TeamsService:
  """
    Teams service
  """
  def __init__(self, teams_repository: TeamsRepository):
    self.teams_repo: TeamsRepository = teams_repository


  # Get list team
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of team
  def get_list(self):
    # Get list team
    payload = jsonable_encoder(self.teams_repo.get_list())

    return payload
