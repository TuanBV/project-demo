"""
Accept offer candidates service
"""

from recruit_mails import MailRepository
from core import CommonException, ERR_MESSAGE
from recruit_templates import TemplatesRepository
from recruit_parameters import ParametersRepository
from recruit_accept_offer_candidates import AcceptOfferCandidatesRepository
from recruit_candidates import CandidatesRepository
from recruit_result_candidates import ResultCandidatesRepository
from helpers.mailer import Mailer
from helpers.const import CODE
from helpers import kbn
from fastapi.encoders import jsonable_encoder

class AcceptOfferCandidatesService:
  """
    Result candidates service
  """
  def __init__(self, mails_repository: MailRepository, templates_repository: TemplatesRepository,
               parameters_repository: ParametersRepository, accept_offer_candidates_repository: AcceptOfferCandidatesRepository,
               candidates_repository: CandidatesRepository, result_candidates_repository: ResultCandidatesRepository):
    self.mails_repo: MailRepository = mails_repository
    self.templates_repo: TemplatesRepository = templates_repository
    self.parameters_repo: ParametersRepository = parameters_repository
    self.accept_offer_candidates_repo: AcceptOfferCandidatesRepository = accept_offer_candidates_repository
    self.candidates_repo: CandidatesRepository = candidates_repository
    self.result_candidates_repo: ResultCandidatesRepository = result_candidates_repository


  # Get list received offer candidate
  # Output:
  #   return: Candidates
  def get_list(self):
    candidates = self.accept_offer_candidates_repo.get_list()
    # Candidate not exist
    if not candidates:
      raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

    return {"candidates": candidates}


  # Edit start join date
  # Param:
  #   @candidate_id: Candidate id
  #   @start_join_date: Start join date
  # Return: None
  def edit_start_join(self, candidate_id: int, start_join_date: str):
    self.accept_offer_candidates_repo.edit_start_join(candidate_id, start_join_date)


  # Send mails link form
  # Param:
  #   @candidates_id: Candidates id
  # Return: None
  async def send_mails(self, candidates_id: list):
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
      self.accept_offer_candidates_repo.add_token(candidate["id"], "")


  # Get candidate by token
  # Param:
  #   @token: Token
  # Return: Candidate
  def get_candidate_by_token(self, token: str):
    return self.accept_offer_candidates_repo.get_candidate_by_token(token)


  # Edit candidate by token
  # Param:
  #   @token: Token
  #   @candidate: Candidate
  # Return: None
  def edit_candidate_by_token(self, token, candidate):
    return self.accept_offer_candidates_repo.edit_candidate_by_token(token, candidate)


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
      if candidate["office_id"] == 1:
        template = self.templates_repo.get_template_by_key("invite_to_work_hn")
      else:
        template = self.templates_repo.get_template_by_key("invite_to_work_hue")

      # Get params in db
      params = self.parameters_repo.get_by_params_name(template["params"])

      if candidate["status"] != kbn.CandidateStatus.ACCEPT_OFFER:
        raise CommonException(message=ERR_MESSAGE.UNABLE_SEND_FORM)

      values = self.parameters_repo.get_key_value_by_params(params, candidate["id"])
      body = template["body"]

      for key in values:
        if key == "$LinkForm":
          body = body.replace(key, str(values[key]["link"]))
        else:
          body = body.replace(key, str(values[key]))

      mail = {
        "title": template["title"],
        "body": body,
        "candidate_id": candidate["id"],
        "status": 0
      }

      # Create mail
      mail_id = self.mails_repo.create_mail(mail)
      mail["id"] = mail_id
      mails.append(mail)

      self.accept_offer_candidates_repo.add_token(candidate["id"], values["$LinkForm"]["token"])

    return { "mails": mails }
