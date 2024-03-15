"""
Service template util
"""
from core.message import ERR_MESSAGE
from helpers.const import MAX_SIZE_PDF
from sqlalchemy import desc, asc
from models import Templates, ActionTypes

# Check file pdf of template
# Params:
#   @template_id: Id template choose
#   @file: File pdf user upload
#   @file_size: Size of file user upload
#   @file_type: Type of file user upload
# Output:
#   return: Boolean
def check_file_pdf_template(template_id, file, file_size, file_type):
  file_size = file_size.strip()
  file_type = file_type.strip()

  # Upload new pdf
  if template_id is None:
    # File pdf is not exist will raise error
    if file != "" and file_size != "" and file_type != "":
      # If file is not pdf or size is too limited will raise error
      if (file_type != "pdf" or int(file_size) > MAX_SIZE_PDF):
        return False
    # Check file pdf is not exist
    else:
      return  False

  return True


# Validate postcard pdf file of template
# Params:
#   @body: Data request
#   @result_template: Data template
# Output:
#   return: List error
def validate_postcard_in_edit(body, result_template):
  # Template type has been changed
  valid = []
  if result_template["action_type"]["name"] != body.action_type.name:
    # File pdf is not exist or file is not pdf or size is too limited will raise error
    if ((body.pdf_post_card == "" and body.pdf_post_card_size == "" and body.pdf_post_card_type == "") or
        (body.body.pdf_post_card_type != "pdf" or int(body.pdf_post_card_size) > MAX_SIZE_PDF)):
      valid.append(ERR_MESSAGE.ERRMSG0166)

  return valid


# Validate flyer pdf file of template
# Params:
#   @body: Data request
#   @result_template: Data template
# Output:
#   return: List error
def validate_flyer_in_edit(body, result_template):
  # Template type has been changed
  valid = []
  if result_template["action_type"]["name"] != body.action_type.name:
    # File pdf first page of Flyer
    # File pdf is not exist or file is not pdf or size is too limited will raise error
    if ((body.pdf_flyer_text != "" and body.pdf_flyer_text_size != "" and body.pdf_flyer_text_type != "") or
        (body.pdf_flyer_text_type != "pdf" or int(body.pdf_flyer_text_size) > MAX_SIZE_PDF)):
      valid.append(ERR_MESSAGE.ERRMSG0167)

    # File pdf second page of Flyer
    # File pdf is not exist or file is not pdf or size is too limited will raise error
    if ((body.pdf_flyer_address != "" and body.pdf_flyer_address_size != "" and body.pdf_flyer_address_type != "") or
        (body.pdf_flyer_address_type != "pdf" or int(body.pdf_flyer_address_size) > MAX_SIZE_PDF)):
      valid.append(ERR_MESSAGE.ERRMSG0168)

  return valid


# Set sort value
# Params:
#   @sort_key: Sort key
#   @sort_type: Sort type
# Output:
#   Return: Sort value
def set_sort_value(sort_key, sort_type):
  column_name = Templates.created_date

  # Set sort_key
  if sort_key == "act_type_name":
    column_name = ActionTypes.name
  elif sort_key != "":
    column_name = Templates.__table__.c[sort_key]

  if sort_type not in ["asc", "desc"]:
    sort_type = "desc"

  # Set query sort
  if sort_type == "asc":
    sort_value = asc(column_name)
  else:
    sort_value = desc(column_name)

  return sort_value
