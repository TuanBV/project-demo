"""
Add Cv Service
"""

from core import CommonException, ERR_MESSAGE
import helpers.const as env
import helpers.kbn as kbn
from helpers.common import no_accent_vietnamese
from recruit_add_cv import AddCvRepository
import time as time_
from utils.date import get_current_time, format_date_time
from dateutil import parser
from fastapi.encoders import jsonable_encoder
import base64
from reportlab.pdfgen import canvas
from setting import settings


class AddCvService:
  """
    Add Cv service
  """
  def __init__(self, add_cv_repository: AddCvRepository):
    self.add_cv_repo: AddCvRepository = add_cv_repository


  # Add candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def add(self, data):
    data["candidate"]["email"] = data["candidate"]["email"].lower()

    folder_cv = "upload/cv"

    # Check upload file or not
    if not data["candidate"]["cv_file"]["file"]:
      raise CommonException(message = ERR_MESSAGE.FILE_MISSING)

    # File is not pdf, xlsx, docx
    if data["candidate"]["cv_file"]["file_ext"] not in ["pdf", "docx", "doc"]:
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

    data["candidate"]["cv_file_path"] = f"{folder_cv}/{file_name}"
    data["candidate"]["created_user"] = data["employee_code"]
    data["candidate"]["application_date"] = get_current_time()

    del data["candidate"]["cv_file"]

    data_candidate_exist = self.add_cv_repo.check_email_exist(data["candidate"]["email"])

    if data_candidate_exist:
      data_candidate_return = jsonable_encoder(self.add_cv_repo.edit(data, data_candidate_exist))
    else:
      data_candidate_return = jsonable_encoder(self.add_cv_repo.add(data))

    data_candidate_return["application_date"] = format_date_time(parser.parse(data_candidate_return["application_date"]), "%Y-%m-%d")
    data_candidate_return["cv_file_path"] = f'{settings.DOMAIN_FILE}/{data_candidate_return["cv_file_path"]}'
    data_candidate_return["office"] = "Hà Nội" if data_candidate_return["office_id"] == kbn.Office.HANOI.value else "Huế"
    if data_candidate_return["gender"] == kbn.Gender.MALE.value:
      data_candidate_return["gender"] = "Nam"
    elif data_candidate_return["gender"] == kbn.Gender.FEMALE.value:
      data_candidate_return["gender"] = "Nữ"
    else:
      data_candidate_return["gender"] = "Không xác định"

    return data_candidate_return


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.add_cv_repo.get_list()

    return payload
