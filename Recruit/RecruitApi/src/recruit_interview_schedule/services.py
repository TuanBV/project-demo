"""
Interview schedule Service
"""

from core import CommonException, ERR_MESSAGE
from recruit_interview_schedule import InterviewScheduleRepository
from helpers.mailer import Mailer

class InterviewScheduleService:
  """
    Interview schedule service
  """
  def __init__(self, interview_schedule_repository: InterviewScheduleRepository):
    self.interview_schedule_repo: InterviewScheduleRepository = interview_schedule_repository


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.interview_schedule_repo.get_list()

    return payload


  # Add interview information
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  async def add_interview_infor(self, data):
    result_interview = self.interview_schedule_repo.get_interview(data["candidate_id"])

    if not result_interview:
      raise CommonException(message = ERR_MESSAGE.INTERVIEW_NOT_FOUND)

    data_mail = self.interview_schedule_repo.add_interview_detail(result_interview, data)

    for mail in data_mail["list_mail"]:
      mail["values"]["$nameInterviewer"] = ", ".join(data_mail["list_interviewer"])

      for key in mail["values"]:
        mail["body"] = mail["body"].replace(key, str(mail["values"][key]))

      # Handle send mail
      mailer = Mailer(username=mail["office"].mail_admin, password=mail["office"].password_mail)
      await mailer.set_mail_from(mail["office"].mail_admin).subject(mail["template"]["title"]).html(mail["body"]).recipient(mail["user"].email
        ).add_attachment(f'./{mail["candidate"].cv_file_path}', list(mail["candidate"].cv_file_path.split("/"))[-1]).send()


  # Edit interview information
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  async def edit_interview_infor(self, data):
    result_interview = self.interview_schedule_repo.get_interview(data["candidate_id"])

    if not result_interview:
      raise CommonException(message = ERR_MESSAGE.INTERVIEW_NOT_FOUND)

    data_mail = self.interview_schedule_repo.edit_interview_detail(result_interview, data)

    for mail in data_mail["list_mail"]:
      mail["values"]["$nameInterviewer"] = ", ".join(data_mail["list_interviewer"])

      for key in mail["values"]:
        mail["body"] = mail["body"].replace(key, str(mail["values"][key]))

      # Handle send mail
      mailer = Mailer(username=mail["office"].mail_admin, password=mail["office"].password_mail)

      if mail["flag_set_cv_file"]:
        mailer.add_attachment(f'./{mail["candidate"].cv_file_path}', list(mail["candidate"].cv_file_path.split("/"))[-1])

      await mailer.set_mail_from(mail["office"].mail_admin).subject(mail["template"]["title"]).html(mail["body"]).recipient(mail["user"].email).send()
