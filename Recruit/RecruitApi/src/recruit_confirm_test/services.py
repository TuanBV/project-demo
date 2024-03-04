"""
Confirm test Service
"""

from core import CommonException, ERR_MESSAGE
from recruit_confirm_test import ConfirmTestRepository
from fastapi.encoders import jsonable_encoder
from helpers.const import CODE


class ConfirmTestService:
  """
    Confirm test service
  """
  def __init__(self, confirm_test_repository: ConfirmTestRepository):
    self.confirm_test_repo: ConfirmTestRepository = confirm_test_repository


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.confirm_test_repo.get_list()

    return payload


  # Save score candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def save_score(self, data):
    result_candidates = self.confirm_test_repo.get_list_save_score(data["list_candidate"])

    if not result_candidates:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    self.confirm_test_repo.save_score(data["list_candidate"], data["employee_code"])


  # Eliminate test
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def eliminate(self, data):
    result_candidate = self.confirm_test_repo.get_candidate(data["candidate_id"])

    if not result_candidate:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    result_interview = self.confirm_test_repo.get_interview(data["candidate_id"])

    if not result_interview:
      raise CommonException(message=ERR_MESSAGE.INTERVIEW_NOT_FOUND)

    self.confirm_test_repo.eliminate(result_candidate, result_interview, data)


  # Eliminate all test
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def eliminate_all(self, data):
    list_id = []
    for candidate in data["list_id"]:
      list_id.append(candidate["id"])

    if not list_id:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    result_candidate_interview = jsonable_encoder(self.confirm_test_repo.get_list_candidate_interview(list_id))

    for candidate_db in result_candidate_interview:
      for candidate_request in data["list_id"]:
        if candidate_db["candidate_id"] == candidate_request["id"]:
          candidate_db["flag_not_test"] = candidate_request["flag_not_test"]

    if not result_candidate_interview:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    self.confirm_test_repo.eliminate_all(result_candidate_interview, data)


  # Confirm all test
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def confirm_all(self, data):
    list_id = []

    for candidate in data["list_id"]:
      list_id.append(candidate)

    if not list_id:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    result_candidate_interview = jsonable_encoder(self.confirm_test_repo.get_list_candidate_interview(list_id))

    if not result_candidate_interview:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    for candidate in result_candidate_interview:
      if not candidate["score"]:
        raise CommonException(message=ERR_MESSAGE.CANDIDATE_NOT_HAVE_SCORE)

    self.confirm_test_repo.confirm_all(result_candidate_interview, data)
