"""
Confirm test repository
"""

from core import CommonRepository, CommonException, ERR_MESSAGE
from models import Candidates, Teams, Interviews, Offices
from helpers import kbn
from helpers.const import MAX_SCORE
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc


class ConfirmTestRepository(CommonRepository):
  """
  Repository of Service confirm test
  """


  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      query_candidates = session.query(Candidates.id, Candidates.fullname, Teams.name.label("team"), Candidates.email, Candidates.telephone_no, Candidates.gender,
        Candidates.status, Interviews.id.label("interview_id"), Interviews.interview_form, Interviews.date, Interviews.test_score.label("score"), Offices.name.label("office")
      ).join(
        Teams, Teams.id == Candidates.team_id
      ).join(
        Interviews, Interviews.candidate_id == Candidates.id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Teams.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.status == kbn.CandidateStatus.TEST.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
        Interviews.type_kbn == kbn.InterviewType.TEST.value,
      ).order_by(desc(Candidates.updated_date))

      # Get count data filter
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


  # Get list candidate save score
  # Params:
  #   @list_score: List candidate update score
  # Output:
  #   return: List candidate
  def get_list_save_score(self, list_score):
    with self.session_factory_read() as session:
      list_id = []
      for score in list_score:
        list_id.append(score["id"])

      result_candidate = session.query(Candidates.id, Interviews.id.label("interview_id")
      ).outerjoin(
        Interviews, Interviews.candidate_id == Candidates.id
      ).filter(Candidates.id.in_(list_id), Interviews.type_kbn == kbn.InterviewType.TEST.value).all()

      return result_candidate


  # Save score
  # Params:
  #   @list_score: List data score
  #   @updated_user: Updater
  # Output:
  #   return: Void
  def save_score(self, list_score, updated_user):
    with self.session_factory() as session:
      for candidate in list_score:
        candidate["score"] = int(candidate["score"]) if candidate["score"] else None
        if candidate["score"] and candidate["score"] > MAX_SCORE:
          raise CommonException(message=ERR_MESSAGE.SCORE_INVALID)

        session.query(Interviews).filter(Interviews.id == candidate["interview_id"]).update({
          Interviews.test_score: candidate["score"],
          Interviews.updated_user: updated_user,
        })

      session.commit()


  # Get data interview
  # Params:
  #   @candidate_id: Id candidate
  # Output:
  #   return: Data interview
  def get_interview(self, candidate_id):
    with self.session_factory_read() as session:
      result_interview = session.query(Interviews).filter(Interviews.candidate_id == candidate_id,
        Interviews.is_deleted == kbn.DeleteFlag.OFF.value,
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value).first()

      return result_interview


  # Eliminate candidate and interview
  # Params:
  #   @candidate: Data candidate
  #   @interview: Data interview
  #   @data: Data request
  # Output:
  #   return: Void
  def eliminate(self, candidate, interview, data):
    with self.session_factory() as session:

      interview_status = kbn.InterviewStatus.FAILED.value if not data["flag_not_test"] else kbn.InterviewStatus.NOT_TEST.value
      candidate_status = kbn.CandidateStatus.FAILED_TEST.value if not data["flag_not_test"] else kbn.CandidateStatus.NOT_TEST.value

      session.query(Interviews).filter(Interviews.id == interview.id).update({
        Interviews.status: interview_status,
        Interviews.updated_user: data["employee_code"],
      })

      session.query(Candidates).filter(Candidates.id == candidate.id).update({
        Candidates.status: candidate_status,
        Candidates.previous_status: candidate.status.value,
        Candidates.count_apply: candidate.count_apply + 1,
        Candidates.updated_user: data["employee_code"],
      })

      session.commit()


  # Get list interview eliminate
  # Params:
  #   @list_score: List candidate update score
  # Output:
  #   return: List candidate
  def get_list_candidate_interview(self, list_id):
    with self.session_factory_read() as session:
      result_candidate = session.query(Candidates.id.label("candidate_id"), Candidates.count_apply, Candidates.status, Candidates.office_id,
        Interviews.id.label("interview_id"), Interviews.test_score.label("score")
      ).outerjoin(
        Interviews, Interviews.candidate_id == Candidates.id
      ).filter(Candidates.id.in_(list_id), Interviews.type_kbn == kbn.InterviewType.TEST.value).all()

      return result_candidate


  # Eliminate all candidate and interview
  # Params:
  #   @list_id: List id candidate and interview
  #   @data: Data request
  # Output:
  #   return: Void
  def eliminate_all(self, list_id, data):
    with self.session_factory() as session:
      for item in list_id:
        interview_status = kbn.InterviewStatus.FAILED.value if not item["flag_not_test"] else kbn.InterviewStatus.NOT_TEST.value
        candidate_status = kbn.CandidateStatus.FAILED_TEST.value if not item["flag_not_test"] else kbn.CandidateStatus.NOT_TEST.value

        session.query(Candidates).filter(Candidates.id == item["candidate_id"]).update({
          Candidates.status: candidate_status,
          Candidates.previous_status: item["status"],
          Candidates.count_apply: item["count_apply"] + 1,
          Candidates.updated_user: data["employee_code"],
        })

        session.query(Interviews).filter(Interviews.id == item["interview_id"]).update({
          Interviews.status: interview_status,
          Interviews.updated_user: data["employee_code"],
        })

      session.commit()


  # Confirm all candidate and interview
  # Params:
  #   @list_id: List id candidate and interview
  #   @data: Data request
  # Output:
  #   return: Void
  def confirm_all(self, list_id, data):
    with self.session_factory() as session:
      new_status = ""
      data_contact = {}
      for item in list_id:
        new_status = kbn.CandidateStatus.TEST_OK.value
        if item["office_id"] == kbn.Office.HUE.value:
          new_status = kbn.CandidateStatus.FIRST_INTERVIEW.value
          interview_data = session.query(Interviews).filter(Interviews.id == item["interview_id"]).first()

          data_contact["date"] = interview_data.date
          data_contact["time"] = interview_data.time
          data_contact["meeting_room_id"] = interview_data.meeting_room_id
          data_contact["type_kbn"] = kbn.InterviewType.FIRST_INTERVIEW.value
          data_contact["candidate_id"] = interview_data.candidate_id
          data_contact["status"] = kbn.InterviewStatus.PREPARE_INTERVIEW.value
          data_contact["link_interview"] = interview_data.link_interview
          data_contact["interview_form"] = interview_data.interview_form.value
          data_contact["created_user"] = data["employee_code"]

          data_contact = Interviews(**data_contact)

          session.add(data_contact)

        session.query(Candidates).filter(Candidates.id == item["candidate_id"]).update({
          Candidates.status: new_status,
          Candidates.previous_status: item["status"],
          Candidates.updated_user: data["employee_code"],
        })

        session.query(Interviews).filter(Interviews.id == item["interview_id"]).update({
          Interviews.status: kbn.InterviewStatus.PASS.value,
          Interviews.updated_user: data["employee_code"],
        })

      session.commit()
