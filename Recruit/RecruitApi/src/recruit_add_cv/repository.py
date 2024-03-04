"""
Add Cv repository
"""

from core import CommonRepository
from models import Candidates, Recommenders, Positions, Teams, Offices
from helpers import kbn
from fastapi.encoders import jsonable_encoder
from setting import settings
from sqlalchemy import desc
from copy import deepcopy
from utils.date import get_current_time


class AddCvRepository(CommonRepository):
  """
  Repository of Service add cv
  """

  # Add candidates
  # Param:
  #   @data: Data request
  # Output:
  #   return: Data candidate
  def add(self, data):
    with self.session_factory() as session:
      data["candidate"]["position_id"] = int(data["candidate"]["position_id"])
      data["candidate"]["team_id"] = int(data["candidate"]["team_id"])
      data["candidate"]["office_id"] = int(data["candidate"]["office_id"])
      data["candidate"]["recommender_id"] = int(data["candidate"]["recommender_id"]) if data["candidate"]["recommender_id"] else None
      data["candidate"]["gender"] = int(data["candidate"]["gender"])
      data["candidate"]["number_experiences"] = float(data["candidate"]["number_experiences"])

      data["candidate"] = Candidates(**data["candidate"])

      session.add(data["candidate"])

      data["candidate"] = data["candidate"].__dict__

      # Execute transaction
      session.commit()

      return data["candidate"]


  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      query_candidates = session.query(Candidates.id, Candidates.fullname, Teams.name.label("team"), Positions.name.label("position"), Candidates.email,
        Candidates.telephone_no, Candidates.status, Candidates.application_date, Candidates.cv_file_path, Candidates.previous_status, Candidates.gender,
        Recommenders.fullname.label("recommender"), Offices.name.label("office")
      ).outerjoin(
        Recommenders, Recommenders.id == Candidates.recommender_id
      ).join(
        Teams, Teams.id == Candidates.team_id
      ).join(
        Positions, Positions.id == Candidates.position_id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Teams.is_deleted == kbn.DeleteFlag.OFF.value,
        Positions.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.status == kbn.CandidateStatus.RECEIVE_CV.value,
      ).order_by(desc(Candidates.created_date))

      data_candidates = jsonable_encoder(query_candidates.all())

      for candidate in data_candidates:
        candidate["cv_file_path"] = f'{settings.DOMAIN_FILE}/{candidate["cv_file_path"]}'
        if candidate["gender"] == kbn.Gender.MALE.value:
          candidate["gender"] = "Nam"
        elif candidate["gender"] == kbn.Gender.FEMALE.value:
          candidate["gender"] = "Nữ"
        else:
          candidate["gender"] = "Không xác định"

      payload["item"] = data_candidates

      return payload


  # Check email candidate exist
  # Params:
  #   @email: Email candidate
  # Output:
  #   return: Bool
  def check_email_exist(self, email):
    with self.session_factory_read() as session:
      return session.query(Candidates).filter(Candidates.email == email).first()


  # Edit candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Data candidate
  def edit(self, data, data_db):
    with self.session_factory() as session:
      data["candidate"]["position_id"] = int(data["candidate"]["position_id"])
      data["candidate"]["team_id"] = int(data["candidate"]["team_id"])
      data["candidate"]["office_id"] = int(data["candidate"]["office_id"])
      data["candidate"]["recommender_id"] = int(data["candidate"]["recommender_id"]) if data["candidate"]["recommender_id"] else None
      data["candidate"]["gender"] = int(data["candidate"]["gender"])
      data["candidate"]["number_experiences"] = float(data["candidate"]["number_experiences"])
      data["candidate"]["updated_user"] = data["employee_code"]
      data["candidate"]["previous_status"] = data_db.status.value
      data["candidate"]["status"] = kbn.CandidateStatus.RECEIVE_CV.value
      data["candidate"]["created_date"] = get_current_time()

      data_candidate = deepcopy(data["candidate"])

      session.query(Candidates).filter(Candidates.id == data_db.id).update(data_candidate)

      # Execute transaction
      session.commit()

      data_candidate = Candidates(**data["candidate"])

      data_candidate.id = data_db.id

      return data_candidate
