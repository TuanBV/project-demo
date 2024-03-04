"""
Candidates list repository
"""

from core import CommonRepository
from models import Candidates, Positions, Teams, Offices, Recommenders
from helpers import kbn
from sqlalchemy import desc, or_, and_
from fastapi.encoders import jsonable_encoder
from setting import settings


class BlackListRepository(CommonRepository):
  """
  Repository of Service black list
  """

  # Get black list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}
      data_candidates = jsonable_encoder(session.query(Candidates.id, Candidates.fullname,
        Teams.name.label("team"), Positions.name.label("position"),
        Candidates.email, Candidates.telephone_no, Candidates.note,
        Offices.name.label("office"), Recommenders.fullname.label("recommender_name"),
        Candidates.cv_file_path, Candidates.status, Candidates.previous_status, Candidates.gender
      ).outerjoin(
        Recommenders, Candidates.recommender_id == Recommenders.id
      ).outerjoin(
        Teams, Teams.id == Candidates.team_id
      ).outerjoin(
        Positions, Positions.id == Candidates.position_id
      ).outerjoin(
        Offices, Offices.id == Candidates.office_id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Teams.is_deleted == kbn.DeleteFlag.OFF.value,
        Positions.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        or_(
          Candidates.count_apply > kbn.CountApply.TWO_APPLY.value,
          Candidates.status == kbn.CandidateStatus.BLACK_LIST.value,
          and_(
            Candidates.count_apply == kbn.CountApply.TWO_APPLY.value,
            Candidates.status.in_([
              kbn.CandidateStatus.FAILED_CV.value, kbn.CandidateStatus.FAILED_TEST.value, kbn.CandidateStatus.NOT_INTERVIEW.value,
              kbn.CandidateStatus.REFUSE_OFFER.value, kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value, kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value
            ])
          )
        )
      ).order_by(desc(Candidates.updated_date)).all())

      for candidate in data_candidates:
        candidate["cv_file_path"] = f'{settings.DOMAIN_FILE}/{candidate["cv_file_path"]}'
        if candidate["gender"] == kbn.Gender.MALE.value:
          candidate["gender"] = "Nam"
        elif candidate["gender"] == kbn.Gender.FEMALE.value:
          candidate["gender"] = "Nữ"
        else:
          candidate["gender"] = "Không xác định"

      # Set data for payload
      payload["item"] = data_candidates

      # Data return
      return payload
