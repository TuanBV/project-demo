"""
Service parameter repository
"""

from core import CommonRepository
from models import Parameters, Candidates, Interviews, Offices, Users, Teams
from helpers import kbn
from helpers.const import DAY_OF_WEEK
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from setting import settings
from models.positions import Positions
from utils.date import format_date_time
from sqlalchemy import asc, desc

class ParametersRepository(CommonRepository):
  """
  Repository of service repository
  """
  # Get list parameter
  # Params: None
  # Output: list parameter and count record
  def get_list(self):
    with self.session_factory_read() as session:
      query = session.query(Parameters).filter(Parameters.is_deleted == kbn.DeleteFlag.OFF.value).order_by(asc(Parameters.id))
      count_param = query.count()

      return {
        "list_param": jsonable_encoder(query.all()),
        "count": count_param,
      }


  # Get parameter by id param
  # Params:
  #   @id_param: id of parameter
  # Output: item parameter
  def get_by_id(self, id_param):
    with self.session_factory_read() as session:
      return session.query(Parameters).filter(Parameters.id == id_param, Parameters.is_deleted == kbn.DeleteFlag.OFF.value).first()


  # Add parameter
  # Param:
  #   @data_param: data request of param
  # Return: None
  def add(self, data_param):
    with self.session_factory() as session:
      param = Parameters(**data_param)
      session.add(param)
      # Commit
      param = param.__dict__
      session.commit()
      return param


  # Edit parameter
  # Param:
  #   @id_param: id of param
  #   @data_param: data request of param
  # Return: None
  def edit(self, id_param, data_param):
    with self.session_factory() as session:
      session.query(Parameters).filter(
        Parameters.id == id_param, Parameters.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Parameters.name: data_param.name,
        Parameters.table: data_param.table,
        Parameters.column: data_param.column,
        Parameters.note: data_param.note,
      })
      session.commit()


  # Delete parameter
  # Param:
  #   @id_param: id of param
  # Return: None
  def delete(self, id_param):
    with self.session_factory() as session:
      session.query(Parameters).filter(Parameters.id == id_param).update({
        Parameters.is_deleted: kbn.DeleteFlag.ON.value
      })
      session.commit()


  # Get parameter by params_name
  # Params:
  #   @params_name: Params name
  # Output: Parameters
  def get_by_params_name(self, list_params: list):
    with self.session_factory_read() as session:
      params = session.query(Parameters).filter(
        Parameters.name.in_(list_params),
        Parameters.is_deleted == kbn.DeleteFlag.OFF.value
      ).all()
      params = jsonable_encoder(params)

      for param in params:
        if param["name"] in list_params:
          list_params.remove(param["name"])

      params += list_params
      return params


  # Generate link form candidate unique
  # Output: Link form candidate
  def generate_link_form(self) -> dict:
    token = uuid4()
    return {
      "token": token,
      "link": f"{settings.FORM_USER_URL}?token={token}"
    }

  # Generate link forgot password
  # Output: Link form candidate
  def generate_link_forgot_password(self) -> dict:
    token = uuid4()
    return {
      "token": token,
      "link": f"{settings.PASSWORD_RESET_URL}?token={token}"
    }


  # Format value date time
  # Params:
  #   @data
  # Output:
  #   return: Value
  def __format_value_date_time(self, column, value):
    if column == "date":
      value = [f'{format_date_time(value[0], "%d/%m/%Y")} ({DAY_OF_WEEK[value[0].weekday()]})']
    elif column == "time":
      value = [f"{str(value[0])[0:5]}"]

    return value


  # Get key and value by params
  # Params:
  #   @params: Params
  #   @candidate_id: Candidate id
  # Output: Key and value params
  def get_key_value_by_params(self, params: list, candidate_id: int = 0, office_id: int = 0, employee_code: str = ""):
    with self.session_factory_read() as session:
      column = ""
      values = {}

      for param in params:
        if isinstance(param, dict):
          column = param["column"]

          if candidate_id > 0:
            if param["table"].lower() == "candidates":
              value = session.query(getattr(Candidates, column)).filter(
                Candidates.id == candidate_id,
                Candidates.is_deleted == kbn.DeleteFlag.OFF.value
              ).one()

            elif param["table"].lower() == "interviews":
              value = session.query(getattr(Interviews, column)).filter(
                Interviews.candidate_id == candidate_id,
                Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
                Interviews.is_deleted == kbn.DeleteFlag.OFF.value
              ).one()

              value = self.__format_value_date_time(column, value)

            elif param["table"].lower() == "teams":
              value = session.query(getattr(Teams, column)).join(
                Candidates, Candidates.team_id == Teams.id
              ).filter(
                Candidates.id == candidate_id,
                Teams.is_deleted == kbn.DeleteFlag.OFF.value
              ).one()

            elif param["table"].lower() == "offices":
              value = session.query(getattr(Offices, column)).filter(Offices.id == office_id).one()

          elif len(employee_code) > 0 and param["table"].lower() == "users":
            value = session.query(getattr(Users, column)).filter(Users.employee_code == employee_code).one()

          values["$" + param["name"]] = value[0]

        else:
          if param == "LinkForm":
            values["$LinkForm"] = self.generate_link_form()
          elif param == "LinkFogotPassword":
            values["$LinkFogotPassword"] = self.generate_link_forgot_password()
          elif param == "TextTitle":
            data_candidates = session.query(Candidates.id, Candidates.fullname,
                                            Candidates.position_id,
                                            Positions.name.label("position_name"),
                                            Candidates.email, Candidates.telephone_no, Candidates.full_address,
                                            Candidates.start_join_date, Candidates.birthday,  Offices.name.label("office")
                                          ).outerjoin(
                                            Positions, Positions.id == Candidates.position_id
                                          ).order_by(desc(Candidates.created_date)
                                          ).filter(
                                            Candidates.id == candidate_id,
                                            Candidates.is_deleted == kbn.DeleteFlag.OFF.value
                                          ).all()
            if data_candidates[0].position_id == kbn.ROLE.INTERN.value:
              values["$TextTitle"] = data_candidates[0].position_name.lower()
            else:
              values["$TextTitle"] = "làm"

      return values
