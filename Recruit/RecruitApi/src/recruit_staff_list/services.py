"""
Staff List Service
"""

from recruit_staff_list import StaffListRepository
from core import CommonException, ERR_MESSAGE

class StaffListService:
  """
    Staff list service
  """
  def __init__(self, staff_list_repository: StaffListRepository):
    self.staff_list_repo: StaffListRepository = staff_list_repository


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.staff_list_repo.get_list()

    return payload


  # Delete candidate
  # Params:
  #   @id_candidate: id of candidate
  # Output:
  #   return: None
  def delete(self, id_candidate):
    # Get candidate by id_candidate
    user = self.staff_list_repo.get_by_id(id_candidate)
    # Check candidate has exist
    if not user:
      raise CommonException(message=ERR_MESSAGE.MSG_0004)

    # Delete user
    self.staff_list_repo.delete(id_candidate)

