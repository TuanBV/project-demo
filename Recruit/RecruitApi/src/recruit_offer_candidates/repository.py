"""
Candidates repository
"""

from core import CommonRepository
from core.message import MESSAGE
from models import Candidates, Positions, Teams, Offices
from helpers import kbn
from sqlalchemy import literal, desc
from fastapi.encoders import jsonable_encoder


class OfferCandidatesRepository(CommonRepository):
  """
  Repository of Service offer candidates
  """


  # Get candidates
  # Output:
  #   return: Candidates list
  def get_list(self):
    with self.session_factory() as session:
      positions = session.query(Positions).filter(Positions.is_deleted == kbn.DeleteFlag.OFF.value).subquery()
      teams = session.query(Teams).filter(Teams.is_deleted == kbn.DeleteFlag.OFF.value).subquery()

      candidates = session.query(
        Candidates.id, Candidates.fullname, Candidates.email, Candidates.cv_file_path, Candidates.gender,
        Candidates.telephone_no, Candidates.position_id, Candidates.team_id,
        positions.c.name.label("position"), teams.c.name.label("team"),
        literal(MESSAGE.CANDIDATE_STATUS.SEND_OFFER).label("status"), Offices.name.label("office")
      ).join(
        positions, positions.c.id == Candidates.position_id
      ).join(
        teams, teams.c.id == Candidates.team_id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.status == kbn.CandidateStatus.SEND_OFFER.value
      ).order_by(desc(Candidates.updated_date)).all()

      data_candidates = jsonable_encoder(candidates)

      for candidate in data_candidates:
        if candidate["gender"] == kbn.Gender.MALE.value:
          candidate["gender"] = "Nam"
        elif candidate["gender"] == kbn.Gender.FEMALE.value:
          candidate["gender"] = "Nữ"
        else:
          candidate["gender"] = "Không xác định"

      return data_candidates
