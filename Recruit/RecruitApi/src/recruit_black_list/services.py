"""
Black List Service
"""

from recruit_black_list import BlackListRepository
from recruit_candidates_list import CandidatesListRepository

class BlackListService:
  """
    Black list service
  """
  def __init__(self, black_list_repository: BlackListRepository, candidates_list_repository: CandidatesListRepository):
    self.black_list_repo: BlackListRepository = black_list_repository
    self.candidate_list_repo: CandidatesListRepository = candidates_list_repository


  # Get black list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.black_list_repo.get_list()

    return payload


  # Get candidate by id
  # Params:
  #   @id_candidate: id of candidate
  # Output:
  #   return: item candidate
  def get_by_id(self, id_candidate):
    # Get list candidates
    payload = self.candidate_list_repo.get_by_id(id_candidate)

    return payload

