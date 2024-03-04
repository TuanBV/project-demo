"""
Candidates List Service
"""

from recruit_candidates_list import CandidatesListRepository
from core import CommonException, ERR_MESSAGE
from reportlab.pdfgen import canvas
from helpers.common import no_accent_vietnamese
import helpers.const as env
import time as time_
import base64

class CandidatesListService:
  """
    Candidates list service
  """
  def __init__(self, candidates_list_repository: CandidatesListRepository):
    self.candidates_list_repo: CandidatesListRepository = candidates_list_repository


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.candidates_list_repo.get_list()

    return payload


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_by_id(self, id_candidate):
    # Get list candidates
    payload = self.candidates_list_repo.get_by_id(id_candidate)

    return payload


  # Edit candidate
  # Params:
  #   @id_candidate: id of candidate
  #   @data: Data request
  # Output: None
  def edit(self, id_candidate, data):
    folder_cv = "upload/cv"

    data["cv_file_path"] = ""
    if data["file"]:
      # Check upload file or not
      if not data["file"]:
        raise CommonException(message = ERR_MESSAGE.FILE_MISSING)

      # File is not pdf, xlsx, docx
      if data["file_ext"] not in ["pdf", "xlsx", "docx"]:
        raise CommonException(message = ERR_MESSAGE.FILE_EXT)

      # file size larger than max size will return an error
      if int(data["file_size"].strip()) > env.MAX_CV_SIZE:
        raise CommonException(message = ERR_MESSAGE.FILE_SIZE)

      file_name ="cv_"+no_accent_vietnamese(data["fullname"]) + "_" + str(time_.time()) + "." + data["file_ext"]

      # Convert file data to base64
      data_pdf = base64.b64decode(data["file"])

      # Create file pdf
      canvas.Canvas(f"{folder_cv}/{file_name}")

      with open(f"{folder_cv}/{file_name}", "wb") as file:
        file.write(data_pdf)

      data["cv_file_path"] = f"{folder_cv}/{file_name}"

    # Edit candidate
    self.candidates_list_repo.edit(id_candidate, data)


  # Move candidate to black list
  # Params:
  #   @id_candidate: id of candidate
  #   @data: Data request
  # Output: None
  def delete(self, id_candidate, data):
    # Get candidate by id
    candidate = self.get_by_id(id_candidate)
    if not candidate:
      raise CommonException(message=ERR_MESSAGE.NOT_FOUND_CANDIDATE)

    # Move candidate to black list
    self.candidates_list_repo.delete(id_candidate, data)
