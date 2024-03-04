"""
Invite interview Service
"""

from core import CommonException, ERR_MESSAGE
from helpers.mailer import Mailer
from helpers import kbn
from helpers.const import CODE
from recruit_invite_interview import InviteInterviewRepository
from recruit_mails import MailRepository
from recruit_templates import TemplatesRepository
from recruit_parameters import ParametersRepository
from fastapi.encoders import jsonable_encoder


class InviteInterviewService:
  """
    Invite interview service
  """
  def __init__(self, invite_interview_repository: InviteInterviewRepository, mails_repository: MailRepository, templates_repository: TemplatesRepository,
      parameters_repository: ParametersRepository):
    self.invite_interview_repo: InviteInterviewRepository = invite_interview_repository
    self.mails_repo: MailRepository = mails_repository
    self.templates_repo: TemplatesRepository = templates_repository
    self.parameters_repo: ParametersRepository = parameters_repository


  # Get list candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: List data of candidate
  def get_list(self):
    # Get list candidates
    payload = self.invite_interview_repo.get_list()

    return payload


  # Set mail template interview offline
  # Params:
  #   @candidate: Data candidate
  # Output:
  #   return: Template
  def __set_mail_template_offline(self, candidate):
    template = None

    if candidate["status"] == kbn.CandidateStatus.INVITE_TEST.value:
      template = self.templates_repo.get_template_by_key("invite_test_off")

    elif candidate["status"] == kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value and candidate["position_id"] == kbn.Positions.INTERNSHIP:
      template = self.templates_repo.get_template_by_key("invite_interview_intern_2_off")

    elif candidate["status"] == kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value and candidate["position_id"] != kbn.Positions.INTERNSHIP:
      template = self.templates_repo.get_template_by_key("invite_interview_empl_1_off")

    elif candidate["status"] == kbn.CandidateStatus.INVITE_SECOND_INTERVIEW.value:
      template = self.templates_repo.get_template_by_key("invite_interview_empl_2_off")

    return template


  # Set mail template interview online
  # Params:
  #   @candidate: Data candidate
  # Output:
  #   return: Template
  def __set_mail_template_online(self, candidate):
    template = None

    if candidate["status"] == kbn.CandidateStatus.INVITE_TEST.value:
      template = self.templates_repo.get_template_by_key("invite_test_onl")

    elif candidate["status"] == kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value and candidate["position_id"] == kbn.Positions.INTERNSHIP:
      template = self.templates_repo.get_template_by_key("invite_interview_intern_2_onl")

    elif candidate["status"] == kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value and candidate["position_id"] != kbn.Positions.INTERNSHIP:
      template = self.templates_repo.get_template_by_key("invite_interview_empl_1_onl")

    elif candidate["status"] == kbn.CandidateStatus.INVITE_SECOND_INTERVIEW.value:
      template = self.templates_repo.get_template_by_key("invite_interview_empl_2_onl")

    return template


  # Create mail invite
  # Params:
  #   @list_candidate_id: List id
  # Output:
  #   return: Data mail
  def create_mail_invite_candidates(self, list_candidate_id):
    result_candidate = jsonable_encoder(self.invite_interview_repo.get_by_list_id(list_candidate_id))

    result_mail = self.invite_interview_repo.get_mail_not_sent(list_candidate_id)

    if result_mail:
      raise CommonException(message=ERR_MESSAGE.CANDIDATE_HAVE_MAIL)

    mails = []
    params = []
    template = None

    for candidate in result_candidate:
      if candidate["interview_form"] == kbn.InterviewForm.OFFLINE.value:
        template = self.__set_mail_template_offline(candidate)

      else:
        template = self.__set_mail_template_online(candidate)

      if not template:
        raise CommonException(message=ERR_MESSAGE.TEMPLATE_NOT_FOUND)

      # Get params in db
      params = self.parameters_repo.get_by_params_name(template["params"])

      values = self.parameters_repo.get_key_value_by_params(params, candidate["id"], candidate["office_id"])

      body = template["body"]

      mail = None

      for key in values:
        body = body.replace(key, str(values[key]))

      mail = {
        "title": template["title"],
        "body": body,
        "candidate_id": candidate["id"],
        "status": 0
      }

      mail_id = self.mails_repo.create_mail(mail)
      mail["id"] = mail_id
      del mail["status"]
      mails.append(mail)

    return { "mails": mails }


  # Send mail invite
  # Params:
  #   @list_candidate_id: List id
  # Output:
  #   return: Void
  async def send_mail_candidates(self, list_candidate_id, user):
    candidates = self.invite_interview_repo.get_list_send_mail(list_candidate_id)

    if not candidates:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    new_status = ""

    for candidate in candidates:
      cc = candidate["carbon_copy"] if candidate["carbon_copy"] else []
      # Handle send mail
      mailer = Mailer(username=candidate["mail_admin"], password=candidate["password_mail"])
      await mailer.set_mail_from(candidate["mail_admin"]).subject(candidate["title"]).html(candidate["body"]).recipient(candidate["email"]).cc(*cc).send()
      # Update status send mail
      self.mails_repo.sent(candidate["mail_id"])

      new_status = kbn.CandidateStatus.TEST.value

      if candidate["status"] == kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value:
        new_status = kbn.CandidateStatus.FIRST_INTERVIEW.value
      elif candidate["status"] == kbn.CandidateStatus.INVITE_SECOND_INTERVIEW.value:
        new_status = kbn.CandidateStatus.SECOND_INTERVIEW.value

      self.invite_interview_repo.update_status(candidate["id"], new_status, candidate["status"], user)

    return candidates
