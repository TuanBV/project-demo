"""
Service action utils
"""

import base64
from helpers import kbn
import helpers.const as env
from core import ERR_MESSAGE, CrmException
import time as time_
from utils.aws import upload_file_to_s3
from models import Actions, ActionTypes
from sqlalchemy import desc, asc

FLYER_SIDES = ["flyer_text", "flyer_address"]


# Validate pdf file
# Params:
#   @list_pdf: List pdf file
#   @action_type_name: Action type name
# Output:
#   return: A list of pdf file
def validate_pdf_file(list_pdf, action_type_name):
  file_response = []
  for index,item in enumerate(list_pdf):
    # Check upload file or not
    if item["pdf_file"] and item["pdf_ext"]:
      # Check pdf not from template table
      # File is not pdf
      if item["pdf_ext"] != "pdf":
        raise CrmException(message = ERR_MESSAGE.ERRMSG0013)

      # file size larger than max size will return an error
      if int(item["pdf_size"].strip()) > env.MAX_SIZE_PDF:
        raise CrmException(message = ERR_MESSAGE.ERRMSG0014)

      # Set name file by actionType Postcard
      file_name ="postcard_" + str(time_.time()) + "." + item["pdf_ext"]

      # convert file data to base64
      data_pdf = base64.b64decode(item["pdf_file"])
      directory = env.S3.DIRECTORY.SHOP.POST_CARD

      # If actionType Flyer will set new name file and directory
      if action_type_name == kbn.ACTION_TYPE_NAME.FLYER:
        file_name = FLYER_SIDES[index] + str(time_.time()) + "." + item["pdf_ext"]

        # convert file data to base64
        directory = env.S3.DIRECTORY.SHOP.FLYER

      # Upload file to S3
      s3_file_key = upload_file_to_s3(file_name, data_pdf, directory, env.FILE_TYPE.PDF)

      # Set response URL of pdf file in s3
      file_response.append(s3_file_key)

  return file_response


# Set file pdf
# Params:
#   @data: Data request
# Output:
#   Return: List of pdf file
def set_file_pdf(data):
  file_response = []
  # Process pdf
  # Check actionType is POST_CARD, FLYER
  if data["data_action"]["action_type"]["name"] in [kbn.ACTION_TYPE_NAME.POST_CARD, kbn.ACTION_TYPE_NAME.FLYER]:
    # Action not choose template
    if not data["data_action"]["template_id"]:
      file_response = validate_pdf_file(data["data_action"]["action_body"]["list_pdf"], data["data_action"]["action_type"]["name"])

  return file_response


# Set sort value
# Params:
#   @sort_key: Sort key
#   @sort_type: Sort type
# Output:
#   Return: Sort value
def set_sort_value(sort_key, sort_type):
  column_name = Actions.created_date

  # Set sort_key
  # Sort by action type name
  if sort_key == "act_type_name":
    column_name = ActionTypes.name
  # Sort by code or name or first delivery time of action
  elif sort_key != "":
    column_name = Actions.__table__.c[sort_key]

  if sort_type not in ["asc", "desc"]:
    sort_type = "desc"

  # Set query sort
  if sort_type == "asc":
    sort_value = asc(column_name)
  else:
    sort_value = desc(column_name)

  return sort_value
