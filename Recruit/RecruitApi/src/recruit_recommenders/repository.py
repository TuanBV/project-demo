"""
Recommenders repository
"""

from core import CommonRepository
from models import Recommenders
from helpers import kbn
from sqlalchemy import desc
from fastapi.encoders import jsonable_encoder
from copy import deepcopy


class RecommendersRepository(CommonRepository):
  """
  Repository of Service recommenders
  """

  # Get list recommenders
  # Output:
  #  return: List recommenders
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      query_recommender = session.query(Recommenders).filter(Recommenders.is_deleted == kbn.DeleteFlag.OFF.value)

      # Sort list recommenders by created_date
      sort_value = desc(Recommenders.created_date)
      query_recommender = query_recommender.order_by(sort_value)
      data_recommenders = query_recommender.all()

      if len(data_recommenders) > 0:
        data_recommenders = jsonable_encoder(query_recommender.all())
      else:
        data_recommenders = []

      payload["item"] = data_recommenders
      return payload


  # Check recommenders email exist
  # Params:
  #   @email: Email of recommender
  # Output:
  #   return: Boolean
  def check_recommenders_email_exist(self, email):
    with self.session_factory_read() as session:
      data_recommender = session.query(Recommenders).filter(Recommenders.email == email).first()

      if data_recommender:
        return True

      return False


  # Check recommenders telephone exist
  # Params:
  #   @telephone_no: Telephone of recommender
  # Output:
  #   return: Boolean
  def check_recommenders_telephone_exist(self, telephone_no):
    with self.session_factory_read() as session:
      data_recommender = session.query(Recommenders).filter(Recommenders.telephone_no == telephone_no).first()

      if data_recommender:
        return True

      return False


  # Check recommenders identification number exist
  # Params:
  #   @identification_number: Identification number of recommender
  # Output:
  #   return: Boolean
  def check_recommenders_ident_number(self, identification_number):
    with self.session_factory_read() as session:
      data_recommender = session.query(Recommenders).filter(Recommenders.identification_number == identification_number).first()

      if data_recommender:
        return True

      return False


  # Add recommender
  # Params:
  #   @data: Data request
  # Output:
  #   return: Recommender
  def add(self, data):
    with self.session_factory() as session:
      data_recommender = Recommenders(**data["recommender"])
      session.add(data_recommender)
      data_recommender = data_recommender.__dict__
      session.commit()
      return data_recommender

  # Get recommender by id
  # Param:
  #   @recommender_id: Recommender id
  # Output:
  #   return: Data recommender
  def get_recommender_by_id(self, recommender_id):
    with self.session_factory_read() as session:
      result_recommender = session.query(Recommenders).filter(Recommenders.id == recommender_id, Recommenders.is_deleted == kbn.DeleteFlag.OFF.value).first()

      return result_recommender


  # Edit recommender
  # Param:
  #   @data: Data request
  # Output:
  #   return: Void
  def edit(self, data):
    with self.session_factory() as session:
      data_recommender = deepcopy(data["recommender"])

      data_recommender["updated_user"] = data["employee_code"]

      session.query(Recommenders).filter(Recommenders.id == data["recommender_id"]).update(data_recommender)

      # Execute transaction
      session.commit()


  # Delete recommender
  # Param:
  #   @data: Data request
  # Output:
  #   return: Void
  def delete(self, data):
    with self.session_factory() as session:

      session.query(Recommenders).filter(Recommenders.id == data["recommender_id"]).update({
        Recommenders.is_deleted: kbn.DeleteFlag.ON.value,
        Recommenders.updated_user: data["employee_code"]
      })

      # Execute transaction
      session.commit()
