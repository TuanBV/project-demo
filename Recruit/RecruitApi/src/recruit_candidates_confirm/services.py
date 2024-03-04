"""
Candidates confirm Service
"""

from core import CommonException, ERR_MESSAGE
from recruit_candidates_confirm import CandidatesConfirmRepository
from fastapi.encoders import jsonable_encoder
from helpers.const import CODE


class CandidatesConfirmService:
  """
    Candidates confirm service
  """
  def __init__(self, candidates_confirm_repository: CandidatesConfirmRepository):
    self.candidates_confirm_repo: CandidatesConfirmRepository = candidates_confirm_repository


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.candidates_confirm_repo.get_list()

    return payload


  # Get candidate by id
  # Params:
  #   @candidate_id: Candidate id
  # Output:
  #   return: Data candidate
  def get_by_id(self, candidate_id):
    result_candidate = jsonable_encoder(self.candidates_confirm_repo.get_by_id(candidate_id))

    # Candidate not exist
    if not result_candidate:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    return result_candidate


  # Confirm candidate
  # Params:
  #   @candidate_id: id of candidate
  # Output: None
  def edit(self, candidate_id):
    result_candidate = self.get_by_id(candidate_id)

    # Candidate not exist
    if not result_candidate:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    # Update candidate
    self.candidates_confirm_repo.edit(candidate_id)
