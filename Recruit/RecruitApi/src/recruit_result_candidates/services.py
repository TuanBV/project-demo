"""
Candidates Service
"""

from core import CommonException, ERR_MESSAGE
from helpers.mailer import Mailer
from helpers import kbn
from helpers.const import CODE
from recruit_result_candidates import ResultCandidatesRepository
from recruit_mails import MailRepository
from recruit_templates import TemplatesRepository
from recruit_parameters import ParametersRepository
from recruit_candidates import CandidatesRepository
from fastapi.encoders import jsonable_encoder

class ResultCandidatesService:
  """
    Result candidates service
  """
  def __init__(self, result_candidates_repository: ResultCandidatesRepository,
               candidates_repository: CandidatesRepository, mails_repository: MailRepository,
               templates_repository: TemplatesRepository, parameters_repository: ParametersRepository):
    self.result_candidates_repo: ResultCandidatesRepository = result_candidates_repository
    self.candidates_repo: CandidatesRepository = candidates_repository
    self.mails_repo: MailRepository = mails_repository
    self.templates_repo: TemplatesRepository = templates_repository
    self.parameters_repo: ParametersRepository = parameters_repository


  # Get interviewed candidates
  # Output:
  # @option_value: value of option
  #   return: List candidates
  def get_interviewed_candidates(self, option_value):
    interviewed_candidates = self.result_candidates_repo.get_interviewed_candidates(option_value)

    # Candidate not exist
    if not interviewed_candidates:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    return {"candidates": interviewed_candidates}


  # Send mail candidates
  # Params:
  #   @candidates_id: Candidates id
  # Output:
  #   return: candidates
  async def send_mail_candidates(self, candidates_id: list):
    candidates = self.result_candidates_repo.get_candidates_by_id(candidates_id)

    if not candidates:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    for candidate in candidates:
      cc = candidate["carbon_copy"] if candidate["carbon_copy"] else []
      # Handle send mail
      mailer = Mailer(username=candidate["mail_admin"], password=candidate["password_mail"])

      if candidate["attached_file"]:
        mailer.add_attachment(f'./{candidate["attached_file"]}', candidate["attached_file_name"])

      await mailer.set_mail_from(candidate["mail_admin"]).subject(candidate["title"]).html(
        candidate["body"]).recipient(candidate["email"]).cc(*cc).send()
      # Update status send mail
      self.mails_repo.sent(candidate["mail_id"])
      # Update result status
      self.result_candidates_repo.update_result_status(candidate)

    return candidates


  # Generate mail candidates by key
  # Params:
  #   @candidates_id: Candidates id
  #   @key_template: Key template
  # Output:
  #   return: Mail
  def generate_mail_candidates_by_key(self, candidate_id, key_template):
    # Get template forgot password
    template = self.templates_repo.get_template_by_key(key_template)
    # Get params in db
    params = self.parameters_repo.get_by_params_name(template["params"])
    # Get value params
    values = self.parameters_repo.get_key_value_by_params(params, candidate_id)

    # Replace param in body and title
    for key in values:
      if key == "$LinkFogotPassword" or key == "$LinkForm":
        template["body"] = template["body"].replace(key, str(values[key]["link"]))
        template["title"] = template["title"].replace(key, str(values[key]["link"]))
      else:
        template["body"] = template["body"].replace(key, str(values[key]))
        template["title"] = template["title"].replace(key, str(values[key]))

    return {
      "title": template["title"],
      "body": template["body"],
      "candidate_id": candidate_id,
      "status": 0
    }


  # Check mail candidates exist
  # Params:
  #   @candidates: Candidates
  # Output:
  #   return: None
  def _check_mail_candidates_exist(self, candidates):
    for candidate in candidates:
      if candidate["mail_id"]:
        raise CommonException(message=ERR_MESSAGE.MAIL_EXIST)


  # Create mail candidates
  # Params:
  #   @candidates_id: Candidates id
  # Output:
  #   return: Candidates mail
  def create_mail_candidates(self, candidates_id: list):
    mails = []

    candidates = self.candidates_repo.get_list_candidate_and_mail_by_list_id(candidates_id)
    candidates = jsonable_encoder(candidates)

    self._check_mail_candidates_exist(candidates)

    for candidate in candidates:
      if candidate["status"] == kbn.CandidateStatus.FAILED_TEST:
        mail = self.generate_mail_candidates_by_key(candidate["id"], "failed_test")
      else:
        # Internship
        if candidate["position_id"] == kbn.Positions.INTERNSHIP.value:
          # First interview failed
          if candidate["status"] == kbn.CandidateStatus.FIRST_INTERVIEW_FAILED:
            mail = self.generate_mail_candidates_by_key(candidate["id"], "first_interview_failed")
          # Offer
          else:
            mail = self.generate_mail_candidates_by_key(candidate["id"], "offer")
        # Staff failed interview
        elif candidate["status"] in [kbn.CandidateStatus.FIRST_INTERVIEW_FAILED, kbn.CandidateStatus.SECOND_INTERVIEW_FAILED]:
          mail = self.generate_mail_candidates_by_key(candidate["id"], "interview_failed")
        # Staff Offer
        else:
          mail = self.generate_mail_candidates_by_key(candidate["id"], "offer")

      # Create mail
      mail_id = self.mails_repo.create_mail(mail)
      mail["id"] = mail_id
      mails.append(mail)
    return { "mails": mails }
