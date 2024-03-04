"""
Staff list repository
"""

from core import CommonRepository
from models import Candidates, Positions, Teams, Offices, Recommenders
from setting import settings
from helpers import kbn
from sqlalchemy import desc, or_
from fastapi.encoders import jsonable_encoder


class StaffListRepository(CommonRepository):
  """
  Repository of staff list
  """

  # Get list staff
  # Params: None
  # Output:
  #  return: List staff
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}
      data_candidates = jsonable_encoder(session.query(Candidates.id, Candidates.fullname,
        Teams.name.label("team"), Positions.name.label("position"),
        Candidates.email, Candidates.telephone_no,Candidates.application_date,
        Offices.name.label("office"), Recommenders.fullname.label("recommender_name"),
        Candidates.cv_file_path, Candidates.status, Candidates.previous_status, Candidates.gender
      ).outerjoin(
        Recommenders, Candidates.recommender_id == Recommenders.id
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
        or_(Candidates.status == kbn.CandidateStatus.ALL_OK.value, Candidates.status == kbn.CandidateStatus.TUTORIAL.value)
      ).order_by(desc(Candidates.updated_date)).all())

      for candidate in data_candidates:
        candidate["cv_file_path"] = f'{settings.DOMAIN_FILE}/{candidate["cv_file_path"]}'

        if candidate["gender"] == kbn.Gender.MALE.value:
          candidate["gender"] = "Nam"
        elif candidate["gender"] == kbn.Gender.FEMALE.value:
          candidate["gender"] = "Nữ"
        else:
          candidate["gender"] = "Không xác định"

      # Get list recommender
      data_recommender = jsonable_encoder(session.query(Recommenders.fullname, Recommenders.id
        ).filter(
          Recommenders.is_deleted == kbn.DeleteFlag.OFF.value
        ).all())

      # Set data for payload
      payload["item"] = data_candidates
      payload["list_recommender"] = data_recommender

      # Data return
      return payload

  # Get candidate by id
  # Params: id_candidate: id of candidate
  # Output:
  #  return: candidate
  def get_by_id(self, id_candidate):
    with self.session_factory_read() as session:
      # Get data of candidate
      return session.query(Candidates).filter(
          Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
          Candidates.id == id_candidate,
        ).first()


  # Delete candidate by id
  # Params: id_candidate: id of candidate
  # Output:
  #  return: None
  def delete(self, id_candidate):
    with self.session_factory() as session:
      session.query(Candidates).filter(
        Candidates.id == id_candidate,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Candidates.is_deleted: kbn.DeleteFlag.ON.value,
      })

      session.commit()
