"""
Offices Service
"""
from recruit_mails import MailRepository
import time as time_
import base64
from reportlab.pdfgen import canvas
from pydantic import BaseModel
import os

class MailService:
  """
    Mail service
  """
  def __init__(self, mails_repository: MailRepository):
    self.mails_repository: MailRepository = mails_repository

  # Update Mail
  # Param: 
  # @mail_id: Mail id
  # @data_mail: Mail
  # Return: Mail
  def update(self, mail_id, data_mail):
    folder_cv = "upload/attach_file"
    mail = self.mails_repository.get(mail_id)

    new_mail = {
      "title": data_mail["title"],
      "body": data_mail["body"],
      "carbon_copy": data_mail["carbon_copy"],
    }

    if isinstance(data_mail["attach_file"], BaseModel):
      new_mail["attached_file_name"] = data_mail["attach_file"].file_name

    # Write file
    if data_mail["attach_file"] and not isinstance(data_mail["attach_file"], str) and data_mail["attach_file"].file:
      file_name ="attach_"+ str(time_.time()) + "." + data_mail["attach_file"].file_ext

      # Convert file data to base64
      data_pdf = base64.b64decode(data_mail["attach_file"].file)

      # Create file pdf
      canvas.Canvas(f"{folder_cv}/{file_name}")

      with open(f"{folder_cv}/{file_name}", "wb") as file:
        file.write(data_pdf)

      new_mail["attached_file"] = f"{folder_cv}/{file_name}"

    if not data_mail["attach_file"]:
      new_mail["attached_file"] = None
      new_mail["attached_file_name"] = None

    # Update mail
    self.mails_repository.update(mail_id, new_mail)

    # Remove old attach file
    if mail.attached_file and "attached_file" in new_mail and mail.attached_file != new_mail["attached_file"]:
      os.remove(mail.attached_file)

    # Get mail updated
    new_mail = self.mails_repository.get(mail_id)
    return new_mail.__dict__
