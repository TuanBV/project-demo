"""
Offices Service
"""
from recruit_offices import OfficesRepository
from fastapi.encoders import jsonable_encoder


class OfficesService:
  """
    Offices service
  """
  def __init__(self, offices_repository: OfficesRepository):
    self.offices_repo: OfficesRepository = offices_repository

  # List office
  # Param: None
  # Return: None
  def get_list(self):
    data_office = self.offices_repo.get_list()
    return {
      "list_office": jsonable_encoder(data_office),
    }


  # Get mail offices
  # Return: Offices
  def get_mail_offices(self):
    offices = self.offices_repo.get_mail_offices()
    return {
      "offices": jsonable_encoder(offices)
    }


  # Edit mail offices
  # Param:
  # @mails: Mails
  # Return: None
  def edit_mail_offices(self, mails: dict):
    self.offices_repo.edit_mail_offices(mails)
