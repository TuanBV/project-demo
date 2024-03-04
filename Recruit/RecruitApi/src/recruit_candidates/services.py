"""
Candidates Service
"""

from core import CommonException, ERR_MESSAGE
import helpers.const as env
from helpers.common import no_accent_vietnamese
from helpers.const import CODE
from recruit_candidates import CandidatesRepository
import time as time_
from fastapi.encoders import jsonable_encoder
import base64
from reportlab.pdfgen import canvas


class CandidatesService:
  """
    Candidates service
  """
  def __init__(self, candidates_repository: CandidatesRepository):
    self.candidates_repo: CandidatesRepository = candidates_repository


  # Get candidate
  # Params:
  #   @candidate_id: Candidate id
  # Output:
  #   return: Data candidate
  def get_candidate(self, candidate_id):
    result_candidate = jsonable_encoder(self.candidates_repo.get_candidate_by_id(candidate_id))

    # Candidate not exist
    if not result_candidate:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    return result_candidate


  # Edit candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def edit(self, data):
    result_candidate = self.candidates_repo.get_candidate_by_id(data["candidate_id"])

    # Candidate not exist
    if not result_candidate:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    data["candidate"]["email"] = data["candidate"]["email"].lower()

    # Check upload file or not
    if data["candidate"]["cv_file"]:
      folder_cv = "upload/cv"
      # File is not pdf, xlsx, docx
      if data["candidate"]["cv_file"]["file_ext"] not in ["pdf", "xlsx", "docx"]:
        raise CommonException(message = ERR_MESSAGE.FILE_EXT)

      # file size larger than max size will return an error
      if int(data["candidate"]["cv_file"]["file_size"].strip()) > env.MAX_CV_SIZE:
        raise CommonException(message = ERR_MESSAGE.FILE_SIZE)

      file_name ="cv_"+no_accent_vietnamese(data["candidate"]["fullname"]) + "_" + str(time_.time()) + "." + data["candidate"]["cv_file"]["file_ext"]

      # Convert file data to base64
      data_pdf = base64.b64decode(data["candidate"]["cv_file"]["file"])

      # Create file pdf
      canvas.Canvas(f"{folder_cv}/{file_name}")

      with open(f"{folder_cv}/{file_name}", "wb") as file:
        file.write(data_pdf)

    data["candidate"]["cv_file_path"] = file_name
    data["candidate"]["updated_user"] = data["employee_code"]

    del data["candidate"]["cv_file"]

    self.candidates_repo.edit(data)


  # Delete candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def delete(self, data):
    result_candidate = self.candidates_repo.get_candidate_by_id(data["candidate_id"])

    # Candidate not exist
    if not result_candidate:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    self.candidates_repo.delete(data)


  # Update status for list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def edit_status(self, data):
    result_candidate = self.candidates_repo.get_list_candidate_by_list_id(data["data_request"]["list_id"])

    if not result_candidate:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    self.candidates_repo.edit_status_list_candidate(result_candidate, data["data_request"]["status"], data["employee_code"])
