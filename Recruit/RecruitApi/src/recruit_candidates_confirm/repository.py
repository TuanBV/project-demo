"""
Candidates confirm repository
"""

from core import CommonRepository
from models import Candidates, Positions, Teams, Offices
from helpers import kbn
from sqlalchemy import desc, case
from fastapi.encoders import jsonable_encoder


class CandidatesConfirmRepository(CommonRepository):
  """
  Repository of candidate confirm
  """

  # Get list confirm candidates
  # Params: None
  # Output:
  #  return: List confirm candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}
      query_candidates = session.query(Candidates.id, Candidates.fullname, Teams.name.label("team"), Positions.name.label("position"), Candidates.email,
        Candidates.telephone_no, Candidates.gender, Offices.name.label("office"),
        case((Candidates.status == kbn.CandidateStatus.SEND_FORM.value, "Đã gửi form"), else_ = "Đã cập nhật form").label("status")
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
        Candidates.status.in_([kbn.CandidateStatus.UPDATED_FORM.value, kbn.CandidateStatus.SEND_FORM.value]),
      ).order_by(desc(Candidates.updated_date))

      # Get data candidate
      data_candidates = jsonable_encoder(query_candidates.all())

      for candidate in data_candidates:
        if candidate["gender"] == kbn.Gender.MALE.value:
          candidate["gender"] = "Nam"
        elif candidate["gender"] == kbn.Gender.FEMALE.value:
          candidate["gender"] = "Nữ"
        else:
          candidate["gender"] = "Không xác định"

      payload["item"] = data_candidates

      return payload


  # Get candidate by id of candidate
  # Params:
  #   @candidate_id: Candidate id
  # Output:
  #   return: Data candidate
  def get_by_id(self, candidate_id):
    with self.session_factory_read() as session:
      result_candidate = session.query(Candidates.id, Candidates.date_issued_identification, Candidates.telephone_no, Candidates.status, Candidates.fullname,
        Candidates.bank_account, Candidates.application_date, Candidates.previous_status, Candidates.email,
        Candidates.bank_branch, Candidates.birthday, Candidates.vehicle_number, Candidates.full_address, Candidates.class_room,
        Candidates.start_join_date, Candidates.place_of_birth, Candidates.school, Candidates.cv_file_path,
        Candidates.place_issued_identification, Candidates.department, Candidates.identification_number, Candidates.recommender_id,
        Teams.name.label("team"), Offices.name.label("office"), Positions.name.label("position"),
      ).outerjoin(
        Offices, Candidates.office_id == Offices.id
      ).outerjoin(
        Teams, Candidates.team_id == Teams.id
      ).outerjoin(
        Positions, Candidates.position_id == Positions.id
      ).filter(Candidates.id == candidate_id, Candidates.is_deleted == kbn.DeleteFlag.OFF.value).first()

      return result_candidate


  # Confirm candidate
  # Params:
  #   @candidate_id: id of candidate
  # Output: None
  def edit(self, candidate_id):
    with self.session_factory() as session:
      session.query(Candidates).filter(
        Candidates.id == candidate_id, Candidates.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Candidates.status: kbn.CandidateStatus.TUTORIAL.value
      })

      # Execute transaction
      session.commit()
