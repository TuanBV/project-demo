"""
Candidate assessment Service
"""

from core import CommonException, ERR_MESSAGE
from helpers.const import CODE
from recruit_candidate_assessment import CandidateAssessmentRepository


class CandidateAssessmentService:
  """
    Candidate assessment service
  """
  def __init__(self, candidate_assessment_repository: CandidateAssessmentRepository):
    self.candidate_assessment_repo: CandidateAssessmentRepository = candidate_assessment_repository


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.candidate_assessment_repo.get_list()

    return payload


  # Assessment candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def assessment(self, data):
    self.candidate_assessment_repo.assessment(data)


  # Admin evaluate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def admin_evaluate(self, data):
    result_candidate = self.candidate_assessment_repo.get_candidate(data["candidate_id"])
    if not result_candidate:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    self.candidate_assessment_repo.admin_evaluate(data, result_candidate)
