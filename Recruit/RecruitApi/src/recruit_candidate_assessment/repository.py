"""
Candidate Assessment repository
"""

from core import CommonRepository
from models import Candidates, Interviews, Positions, Teams, Offices, InterviewDetails, Users, MeetingRooms
from helpers import kbn
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc


class CandidateAssessmentRepository(CommonRepository):
  """
  Repository of Service candidate assessment
  """


  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      query_candidates = session.query(Candidates.id, Candidates.fullname, Candidates.email, Candidates.telephone_no, Teams.name.label("team"), Positions.name.label("position"),
        Candidates.status, Candidates.gender, Offices.name.label("office"), Interviews.id.label("interview_id"), Interviews.time, Interviews.date,
        Interviews.meeting_room_id, MeetingRooms.name.label("meeting_room"),
      ).join(
        Teams, Teams.id == Candidates.team_id
      ).join(
        Positions, Positions.id == Candidates.position_id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).join(
        Interviews, Interviews.candidate_id == Candidates.id
      ).outerjoin(
        MeetingRooms, MeetingRooms.id == Interviews.meeting_room_id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Teams.is_deleted == kbn.DeleteFlag.OFF.value,
        Positions.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        Interviews.is_deleted == kbn.DeleteFlag.OFF.value,
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
        Interviews.type_kbn.in_([kbn.InterviewType.FIRST_INTERVIEW.value, kbn.InterviewType.SECOND_INTERVIEW.value]),
        Interviews.meeting_room_id.is_not(None),
        Candidates.status.in_(
          [kbn.CandidateStatus.FIRST_INTERVIEW.value,
          kbn.CandidateStatus.SECOND_INTERVIEW.value]),
      ).order_by(desc(Candidates.updated_date))

      data_candidates = jsonable_encoder(query_candidates.all())

      for candidate in data_candidates:
        if candidate["time"]:
          candidate["time"] = candidate["time"][0:5]

        if candidate["gender"] == kbn.Gender.MALE.value:
          candidate["gender"] = "Nam"
        elif candidate["gender"] == kbn.Gender.FEMALE.value:
          candidate["gender"] = "Nữ"
        else:
          candidate["gender"] = "Không xác định"

        candidate["employee"] = jsonable_encoder(
          session.query(InterviewDetails.id, InterviewDetails.employee_code, Users.fullname, InterviewDetails.comment, InterviewDetails.evaluate
          ).join(
            Users, Users.employee_code == InterviewDetails.employee_code
          ).filter(
            InterviewDetails.interview_id == candidate["interview_id"],
            InterviewDetails.is_deleted == kbn.DeleteFlag.OFF.value,
          ).all())

      payload["item"] = data_candidates

      return payload


  # Prepare data update candidate failed
  # Param:
  #   @data: Data user
  #   @result_candidate: Data update
  # Output:
  #   return: Data update interview and candidate
  def prepare_data_update_failed(self, data, result_candidate):
    new_status = kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value
    if result_candidate.status == kbn.CandidateStatus.SECOND_INTERVIEW.value:
      new_status = kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value

    data_update_candidate = {
      Candidates.status: new_status,
      Candidates.previous_status: result_candidate.status.value,
      Candidates.count_apply: result_candidate.count_apply + 1,
      Candidates.updated_user: data["employee_code"]
    }

    data_update_interview = {
      Interviews.status: kbn.InterviewStatus.FAILED.value,
      Interviews.updated_user: data["employee_code"]
    }

    return {
      "interview": data_update_interview,
      "candidate": data_update_candidate
    }


  # Prepare data update candidate pass
  # Param:
  #   @data: Data user
  #   @result_candidate: Data update
  # Output:
  #   return: Data update interview and candidate
  def prepare_data_update_pass(self, data, result_candidate):
    new_status = kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value
    if result_candidate.status == kbn.CandidateStatus.SECOND_INTERVIEW.value:
      new_status = kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value

    data_update_candidate = {
      Candidates.status: new_status,
      Candidates.previous_status: result_candidate.status.value,
      Candidates.updated_user: data["employee_code"]
    }

    data_update_interview = {
      Interviews.status: kbn.InterviewStatus.PASS.value,
      Interviews.updated_user: data["employee_code"]
    }

    return {
      "interview": data_update_interview,
      "candidate": data_update_candidate
    }


  # Prepare update data
  # Param:
  #   @data: Data user
  #   @result_candidate: Data update
  # Output:
  #   return: Data update interview and candidates
  def prepare_update_data(self, data, result_candidate):
    if int(data["evaluate"]) == kbn.Evaluate.PASS.value:
      return self.prepare_data_update_pass(data, result_candidate)
    else:
      return self.prepare_data_update_failed(data, result_candidate)


  # Check evaluate flag
  # Param:
  #   @result_interview_detail: Data update
  # Output:
  #   return: Flag evaluate failed and flag not evaluate
  def check_evaluate(self, result_interview_detail):
    # Cờ check người đánh giá failed
    flag_evaluate_failed = False
    # Cờ check có người chưa đánh giá
    flag_not_evaluate = False
    for inter_detail_item in result_interview_detail:
      if inter_detail_item.evaluate == kbn.Evaluate.FAILED.value:
        flag_evaluate_failed = True
      elif inter_detail_item.evaluate == kbn.Evaluate.NOT_INTERVIEW_YET.value:
        flag_not_evaluate = True

    return {
      "flag_evaluate_failed": flag_evaluate_failed,
      "flag_not_evaluate": flag_not_evaluate
    }


  # Assessment candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def assessment(self, data):
    with self.session_factory() as session:
      session.query(InterviewDetails).filter(InterviewDetails.id == data["id"]).update({
        InterviewDetails.comment: data["comment"],
        InterviewDetails.evaluate: int(data["evaluate"]),
        InterviewDetails.updated_user: data["employee_code"]
      })

      if int(data["evaluate"]) != kbn.Evaluate.NOT_INTERVIEW_YET.value:

        result_interviews = session.query(Interviews).filter(
          Interviews.candidate_id == data["candidate_id"],
          Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
          Interviews.type_kbn.in_([kbn.InterviewType.FIRST_INTERVIEW.value, kbn.InterviewType.SECOND_INTERVIEW.value]),
          Interviews.is_deleted == kbn.DeleteFlag.OFF.value).first()

        result_interview_detail = session.query(InterviewDetails).filter(
          InterviewDetails.interview_id == result_interviews.id,
          InterviewDetails.id != data["id"],
          InterviewDetails.is_deleted == kbn.DeleteFlag.OFF.value
        ).all()

        result_candidate = session.query(Candidates).filter(Candidates.id == data["candidate_id"], Candidates.is_deleted == kbn.DeleteFlag.OFF.value).first()

        data_update = {}
        # Have only 1 user interview
        if not result_interview_detail:
          data_update = self.prepare_update_data(data, result_candidate)
        # Have 2 or more user interview
        else:
          data_flag_evaluate = self.check_evaluate(result_interview_detail)
          # Flag check have user evaluate FAILED
          flag_evaluate_failed = data_flag_evaluate["flag_evaluate_failed"]
          # Flag check user not evaluate yet
          flag_not_evaluate = data_flag_evaluate["flag_not_evaluate"]

          # Have user evaluate FAILED and all user evaluate
          if flag_evaluate_failed and not flag_not_evaluate:
            data_update = self.prepare_data_update_failed(data, result_candidate)
          # Don't have user evaluate FAILED and all user evaluate
          elif not flag_evaluate_failed and not flag_not_evaluate:
            data_update = self.prepare_update_data(data, result_candidate)

        if "interview" in data_update and "candidate" in data_update and data_update["interview"] and data_update["candidate"]:
          session.query(Candidates).filter(Candidates.id == result_candidate.id).update(data_update["candidate"])
          session.query(Interviews).filter(Interviews.id == result_interviews.id).update(data_update["interview"])

      session.commit()


  # Admin assessment failed
  # Params:
  #   @data: Data request
  #   @result_candidate: Data candidate
  # Output:
  #   return: Void
  def admin_evaluate(self, data, result_candidate):
    with self.session_factory() as session:
      add_count_apply = 0
      if not data["evaluate"]:
        new_candidate_status = kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value if result_candidate.status.value == kbn.CandidateStatus.FIRST_INTERVIEW.value else \
          kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value

        new_interviews_status = kbn.InterviewStatus.FAILED.value
        new_interview_details_status = kbn.Evaluate.FAILED.value
        add_count_apply = 1

      else:
        new_candidate_status = kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value if result_candidate.status.value == kbn.CandidateStatus.FIRST_INTERVIEW.value else \
          kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value

        new_interviews_status = kbn.InterviewStatus.PASS.value
        new_interview_details_status = kbn.Evaluate.PASS.value

      session.query(Candidates).filter(Candidates.id == data["candidate_id"]).update({
        Candidates.status: new_candidate_status,
        Candidates.previous_status: result_candidate.status.value,
        Candidates.count_apply: result_candidate.count_apply + add_count_apply,
        Candidates.updated_user: data["employee_code"]
      })

      result_interview = session.query(Interviews).filter(Interviews.candidate_id == result_candidate.id, Interviews.is_deleted == kbn.DeleteFlag.OFF.value,
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value).first()

      session.query(Interviews).filter(Interviews.id == result_interview.id).update({
        Interviews.status: new_interviews_status,
        Interviews.updated_user: data["employee_code"]
      })

      session.query(InterviewDetails).filter(InterviewDetails.interview_id == result_interview.id, InterviewDetails.evaluate == kbn.Evaluate.NOT_INTERVIEW_YET.value).update({
        InterviewDetails.evaluate: new_interview_details_status,
        InterviewDetails.updated_user: data["employee_code"]
      })

      session.commit()
