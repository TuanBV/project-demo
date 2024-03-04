"""
Office repository
"""

from core import CommonRepository
from models import Mails
from helpers import kbn
from helpers import context

class MailRepository(CommonRepository):
  """
  Repository of Service offices
  """

  # Get mail
  # @mail_id: Mail id
  # Output:
  #   return: void
  def get(self, mail_id):
    with self.session_factory_read() as session:
      return session.query(Mails).filter(Mails.id == mail_id, Mails.is_deleted == kbn.DeleteFlag.OFF.value).first()


  # Update mail
  # Param:
  # @mail_id: Mail id
  # @data_mail: Mail
  # Output:
  #   return: void
  def update(self, mail_id, data_mail):
    with self.session_factory_read() as session:
      session.query(Mails).filter(
        Mails.id == mail_id,
        Mails.is_deleted == kbn.DeleteFlag.OFF.value
      ).update(data_mail)
      session.commit()


  # Update status sent mail
  # Param:
  # @mail_id: int mail id
  # Output:
  #   return: void
  def sent(self, mail_id):
    with self.session_factory_read() as session:
      session.query(Mails).filter(
        Mails.id == mail_id,
        Mails.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Mails.status: kbn.MailFlag.SENT.value,
        Mails.updated_user: context.user.value["employee_code"]
      })
      session.commit()


  # Create mail
  # Param:
  # @mail: Mail
  # Output:
  #   return: Mail id
  def create_mail(self, mail):
    with self.session_factory() as session:
      mail = Mails(**mail)
      session.add(mail)
      session.commit()
      return mail.id


  # Get template by id candidate
  # Params:
  #   @id_candidate: id of candidate
  # Output: item template
  def get_by_id_candidate(self, id_candidate):
    with self.session_factory_read() as session:
      return session.query(Mails.title, Mails.body, Mails.carbon_copy
            ).filter(Mails.candidate_id == id_candidate, Mails.is_deleted == kbn.DeleteFlag.OFF.value, Mails.status == kbn.MailFlag.UNSENT.value).first()

