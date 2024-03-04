"""
Candidates Service
"""

from recruit_offer_candidates import OfferCandidatesRepository
from core import CommonException, ERR_MESSAGE
from helpers.const import CODE

class OfferCandidatesService:
  """
    Result candidates service
  """
  def __init__(self, offer_candidates_repository: OfferCandidatesRepository):
    self.offer_candidates_repo: OfferCandidatesRepository = offer_candidates_repository


  # Get list offer candidate
  # Output:
  #   return: Candidates
  def get_list(self):
    candidates = self.offer_candidates_repo.get_list()
    # Candidate not exist
    if not candidates:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)
    return {"candidates": candidates}

