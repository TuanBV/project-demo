"""
Candidates list repository
"""

from core import CommonRepository
from models import Candidates, Positions, Teams, Offices, Interviews, InterviewDetails, Recommenders, Mails, Users
from setting import settings
from helpers import kbn
from helpers.const import INTERVIEW_STATUS, TYPE_KBN
from sqlalchemy import desc
from fastapi.encoders import jsonable_encoder


class CandidatesListRepository(CommonRepository):
  """
  Repository of candidate list
  """

  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}
      data_candidates = jsonable_encoder(session.query(Candidates.id, Candidates.fullname, Candidates.gender,
        Teams.name.label("team"), Positions.name.label("position"),
        Candidates.email, Candidates.telephone_no,Candidates.application_date,
        Offices.name.label("office"), Recommenders.fullname.label("recommender_name"),
        Candidates.cv_file_path, Candidates.status, Candidates.previous_status
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
        Candidates.count_apply < kbn.CountApply.TWO_APPLY.value,
        Candidates.status.not_in([kbn.CandidateStatus.ALL_OK.value, kbn.CandidateStatus.BLACK_LIST.value])
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


  # Get info of candidate
  # Params:
  #   @id_candidate: id of candidate
  # Output:
  #  return: item candidate and list interview
  def get_by_id(self, id_candidate):
    with self.session_factory_read() as session:
      # Get data of candidate
      data_candidate = jsonable_encoder(session.query(Candidates.id, Candidates.fullname, Candidates.cv_file_path,
          Candidates.team_id, Candidates.position_id, Candidates.full_address,
          Candidates.email, Candidates.telephone_no, Candidates.note, Candidates.birthday,
          Candidates.recommender_id, Candidates.status, Candidates.application_date,
        ).outerjoin(
          Offices, Offices.id == Candidates.office_id
        ).filter(
          Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
          Teams.is_deleted == kbn.DeleteFlag.OFF.value,
          Positions.is_deleted == kbn.DeleteFlag.OFF.value,
          Offices.is_deleted == kbn.DeleteFlag.OFF.value,
          Candidates.id == id_candidate,
          Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        ).first())
      data_candidate["cv_file_path"] = f'{settings.DOMAIN_FILE}/{data_candidate["cv_file_path"]}'

      # Get data of interview
      interviews = jsonable_encoder(session.query(
          Interviews.date.label("time"), Interviews.status, InterviewDetails.comment, Users.fullname, Interviews.type_kbn,
        ).outerjoin(
          InterviewDetails, Interviews.id == InterviewDetails.interview_id
        ).outerjoin(
          Users, InterviewDetails.employee_code == Users.employee_code
        ).filter(
          Interviews.candidate_id == id_candidate
        ).order_by(desc(Interviews.date)).all())
      for item_interview in interviews:
        item_interview["status"] = INTERVIEW_STATUS[item_interview["status"]]
        item_interview["type_kbn"] = TYPE_KBN[item_interview["type_kbn"]]

      # Data return
      payload = {
        "candidate": data_candidate,
        "list_interview": interviews
      }

      return payload


  # Check email of candidate exist
  # Params:
  #   @id_candidate: id of candidate
  #   @email: value of email new
  # Output: boolean
  def check_email(self, email, id_candidate):
    with self.session_factory_read() as session:
      candidate = session.query(Candidates).filter(
        Candidates.email == email,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value
      )

      # If email can use
      if not candidate.first() or candidate.filter(Candidates.id == id_candidate).first():
        return True

      return False


  # Edit candidate
  # Params:
  #   @id_candidate: id of candidate
  #   @data: data request
  # Output: None
  def edit(self, id_candidate, data):
    with self.session_factory() as session:
      if data["cv_file_path"]:
        session.query(Candidates).filter(
          Candidates.id == id_candidate,
          Candidates.is_deleted == kbn.DeleteFlag.OFF.value
        ).update({
          Candidates.cv_file_path: data["cv_file_path"]
        })
      if not data["recommender_id"]:
        data["recommender_id"] = 0

      session.query(Candidates).filter(
        Candidates.id == id_candidate,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Candidates.email: data["email"],
        Candidates.fullname: data["fullname"],
        Candidates.birthday: data["birthday"],
        Candidates.recommender_id: data["recommender_id"],
        Candidates.full_address: data["full_address"],
        Candidates.telephone_no: data["telephone_no"],
        Candidates.position_id: data["position_id"],
        Candidates.team_id: data["team_id"],
        Candidates.status: data["status"],
        Candidates.note: data["note"],
      })

      if data["status"] == kbn.CandidateStatus.RECEIVE_CV.value:
        session.query(Mails).filter(Mails.candidate_id == id_candidate).delete()
        list_id_interview = []
        interviews = session.query(Interviews.id).filter(Interviews.candidate_id == id_candidate).all()
        for item in interviews:
          list_id_interview.append(item.id)
        session.query(Interviews).filter(Interviews.candidate_id == id_candidate).delete()
        session.query(InterviewDetails).filter(InterviewDetails.interview_id.in_(list_id_interview)).delete()
        session.query(Candidates).filter(
          Candidates.id == id_candidate,
          Candidates.is_deleted == kbn.DeleteFlag.OFF.value
        ).update({
          Candidates.result_status: kbn.CandidateResultStatus.UNSENT.value
        })
      session.commit()


  # MOve candidate to black list
  # Params:
  #   @id_candidate: id of candidate
  #   @data: data request
  # Output: None
  def delete(self, id_candidate, data):
    with self.session_factory() as session:
      session.query(Candidates).filter(
        Candidates.id == id_candidate,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Candidates.status: kbn.CandidateStatus.BLACK_LIST.value,
        Candidates.reason: data["reason"],
      })

      session.commit()
