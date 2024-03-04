"""
Candidates List Service
"""

from recruit_candidates_pass_list import CandidatesPassListRepository
from recruit_mails import MailRepository
from recruit_templates import TemplatesRepository
from recruit_parameters import ParametersRepository
from helpers.mailer import Mailer
import re

class CandidatesPassListService:
  """
    Candidates list service
  """
  def __init__(self, candidates_pass_list_repository: CandidatesPassListRepository,mails_repository: MailRepository,
              templates_repository: TemplatesRepository, parameters_repository: ParametersRepository):
    self.candidates_pass_list_repo: CandidatesPassListRepository = candidates_pass_list_repository
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
    payload = self.candidates_pass_list_repo.get_list()

    return {"item": payload}


  # Send mail candidate
  # Params:
  #   @list_id_candidate: list id candidate
  # Output:
  #   return: list mail
  async def send_mail(self, list_id_candidate):
    # Get params in db
    for id_candidate in list_id_candidate:
      # Get email of candidate and email of office
      result = self.candidates_pass_list_repo.get_email(id_candidate)

      # Get template mail of candidate
      template_mail = self.mails_repo.get_by_id_candidate(id_candidate)

      body = template_mail.body
      title = template_mail.title

      # Handle send mail
      mailer = Mailer(username=result.mail_admin, password=result.password_mail)
      await mailer.set_mail_from(result.mail_admin).subject(title).html(body).recipient(result.email).send()

    # Update status mail when send mail for candidate
    self.candidates_pass_list_repo.update_status_mail(list_id_candidate)


  # Add mail candidate
  # Params:
  #   @list_id_candidate: list id candidate
  # Output:
  #   return: list mail
  def add_mail(self, list_id_candidate):
    mails = []
    template = self.templates_repo.get_template_by_key("results_rejected_candidates_hn")
    # Get params in db
    params = self.parameters_repo.get_by_params_name(template["params"])

    for candidate_id in list_id_candidate:
      values = self.parameters_repo.get_key_value_by_params(params, candidate_id)
      body = template["body"]
      title = template["title"]
      mail = None

      for key in values:
        body = body.replace(key, str(values[key]))
        title = title.replace(key, str(values[key]))

      mail = {
        "title": title,
        "body": body,
        "candidate_id": candidate_id,
        "status": 0
      }

      # Add mail for mail table
      mail_id = self.mails_repo.create_mail(mail)
      mail["id"] = mail_id
      mail["status"] = "Chưa gửi"
      mails.append(mail)

    return { "mails": mails }


  # Edit mail candidate
  # Params:
  #   @data: data request
  # Output:
  #   return: item mail
  def edit_mail(self, data):
    # Init
    list_params = []
    list_params.extend(re.findall("\\$[A-Za-z\_]+", data.title))
    list_params.extend(re.findall("\\$[A-Za-z\_]+", data.body))
    for index, param in enumerate(list_params):
      list_params[index] = param.replace("$", "")
    list_params = list(set(list_params))

    # Get params in db
    params = self.parameters_repo.get_by_params_name(list_params)

    values = self.parameters_repo.get_key_value_by_params(params, data.candidate_id)
    body = data.body
    title = data.title
    mail = None

    for key in values:
      body = body.replace(key, str(values[key]))
      title = title.replace(key, str(values[key]))

    mail = {
      "id": data.id,
      "title": title,
      "body": body,
      "candidate_id": data.candidate_id,
      "carbon_copy": data.list_email_cc
    }

    # Update mail of candidate
    self.mails_repo.update(data.id, mail)

    return mail
