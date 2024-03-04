"""
Contact candidate Service
"""

from core import CommonException, ERR_MESSAGE
from recruit_contact_candidate import ContactCandidateRepository


class ContactCandidateService:
  """
    Contact candidate service
  """
  def __init__(self, contact_candidate_repository: ContactCandidateRepository):
    self.contact_candidate_repo: ContactCandidateRepository = contact_candidate_repository


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.contact_candidate_repo.get_list()

    return payload


  # Add contact
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def add(self, data):

    data_candidate = self.contact_candidate_repo.get_candidate(int(data["candidate"]["candidate_id"]))

    if not data_candidate:
      raise CommonException(message = ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    self.contact_candidate_repo.add(data, data_candidate)
