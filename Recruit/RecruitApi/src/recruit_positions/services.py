"""
Positions Service
"""

from recruit_positions import PositionsRepository
from fastapi.encoders import jsonable_encoder


class PositionsService:
  """
    Positions service
  """
  def __init__(self, positions_repository: PositionsRepository):
    self.positions_repo: PositionsRepository = positions_repository


  # Get list position
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of position
  def get_list(self):
    # Get list position
    payload = jsonable_encoder(self.positions_repo.get_list())

    return payload
