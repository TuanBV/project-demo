"""
Office repository
"""

from core import CommonRepository
from models import Offices
from helpers import kbn

class OfficesRepository(CommonRepository):
  """
  Repository of Service offices
  """

  # Get list office
  # Params:
  # Output:
  #   return: list office
  def get_list(self):
    with self.session_factory_read() as session:
      return session.query(Offices).filter(Offices.is_deleted == kbn.DeleteFlag.OFF.value).all()


  # Get mail offices
  # Output:
  #   return: Offices
  def get_mail_offices(self):
    with self.session_factory_read() as session:
      return session.query(Offices.id, Offices.mail_admin).filter(
        Offices.is_deleted == kbn.DeleteFlag.OFF.value
      ).all()


  # Edit mail offices
  # Param:
  # @mails: Mails
  # Return: None
  def edit_mail_offices(self, mails: dict):
    with self.session_factory_read() as session:
      office_setting = kbn.Office.HANOI.value
      if int(mails["office"]) == kbn.Office.HUE.value:
        office_setting = kbn.Office.HUE.value

      session.query(Offices).filter(Offices.id == office_setting).update({
        "mail_admin": mails["mail"],
        "password_mail": mails["password"]
      })

      session.commit()

  # Get office by id
  # Param:
  # @office_id: Office id
  # Return: Office
  def find(self, office_id: int):
    with self.session_factory_read() as session:
      return session.query(Offices).filter(Offices.id == office_id).first()
