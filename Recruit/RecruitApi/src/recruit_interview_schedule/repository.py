"""
Interview schedule repository
"""

from core import CommonRepository
from recruit_templates import TemplatesRepository
from recruit_offices import OfficesRepository
from recruit_meeting_rooms import MeetingRoomsRepository
from recruit_parameters import ParametersRepository
from recruit_users import UsersRepository
from recruit_teams import TeamsRepository
from recruit_candidates import CandidatesRepository
from recruit_positions import PositionsRepository
from models import Candidates, Positions, Teams, Offices, Interviews, InterviewDetails, Users, MeetingRooms
from helpers import kbn
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from setting import settings


class InterviewScheduleRepository(CommonRepository):
  """
  Repository of Service interview schedule
  """


  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      result_meeting_room = session.query(MeetingRooms).filter(MeetingRooms.is_deleted == kbn.DeleteFlag.OFF.value).all()

      query_candidates = session.query(Candidates.id, Candidates.fullname, Candidates.cv_file_path, Teams.name.label("team"), Positions.name.label("position"),
        Candidates.status, Offices.name.label("office"), Interviews.id.label("interview_id"), Interviews.time, Interviews.interview_form, Interviews.date,
        Interviews.meeting_room_id, Candidates.gender
      ).join(
        Teams, Teams.id == Candidates.team_id
      ).join(
        Positions, Positions.id == Candidates.position_id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).join(
        Interviews, Interviews.candidate_id == Candidates.id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Teams.is_deleted == kbn.DeleteFlag.OFF.value,
        Positions.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        Interviews.is_deleted == kbn.DeleteFlag.OFF.value,
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
        Interviews.type_kbn.in_([kbn.InterviewType.FIRST_INTERVIEW.value, kbn.InterviewType.SECOND_INTERVIEW.value]),
        Candidates.status.in_([kbn.CandidateStatus.FIRST_INTERVIEW.value, kbn.CandidateStatus.SECOND_INTERVIEW.value]),
      ).order_by(desc(Candidates.updated_date))

      data_candidates = jsonable_encoder(query_candidates.all())

      for candidate in data_candidates:
        candidate["cv_file_path"] = f'{settings.DOMAIN_FILE}/{candidate["cv_file_path"]}'

        if candidate["gender"] == kbn.Gender.MALE.value:
          candidate["gender"] = "Nam"
        elif candidate["gender"] == kbn.Gender.FEMALE.value:
          candidate["gender"] = "Nữ"
        else:
          candidate["gender"] = "Không xác định"

        if candidate["time"]:
          candidate["time"] = candidate["time"][0:5]

        candidate["date"] = candidate["date"].replace("-", "/")

        candidate["employee"] = jsonable_encoder(
          session.query(InterviewDetails.id, InterviewDetails.employee_code,Users.fullname,
          ).join(
            Users, Users.employee_code == InterviewDetails.employee_code
          ).filter(
            InterviewDetails.interview_id == candidate["interview_id"],
            InterviewDetails.is_deleted == kbn.DeleteFlag.OFF.value,
          ).all())

        for room in result_meeting_room:
          if candidate["meeting_room_id"] == room.id:
            candidate["meeting_room"] = room.name

      payload["item"] = data_candidates

      return payload


  # Get data interview by candidate id
  # Params:
  #   @candidate_id: Candidate id
  # Output:
  #   return: Data interview
  def get_interview(self, candidate_id):
    with self.session_factory_read() as session:
      return session.query(Interviews).filter(Interviews.candidate_id == candidate_id,
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW,
        Interviews.is_deleted == kbn.DeleteFlag.OFF.value).first()


  # Create mail interview
  # Params:
  #   @user: Data user
  #   @employee: Data employee
  #   @data: Data request
  #   @result_interview: Data interview
  #   @template_key: Key of template
  # Output:
  #   return: Data mail
  def create_mail_interview(self, user, employee, data, result_interview, template_key):
    offices_repo = OfficesRepository(self.session_factory, self.session_factory_read)
    meeting_room_repo = MeetingRoomsRepository(self.session_factory, self.session_factory_read)
    team_repo = TeamsRepository(self.session_factory, self.session_factory_read)
    candidate_repo = CandidatesRepository(self.session_factory, self.session_factory_read)
    parameters_repo = ParametersRepository(self.session_factory, self.session_factory_read)
    templates_repo = TemplatesRepository(self.session_factory, self.session_factory_read)
    position_repo = PositionsRepository(self.session_factory, self.session_factory_read)

    flag_set_cv_file = False

    candidate = candidate_repo.get_candidate_by_id(result_interview.candidate_id)
    position = position_repo.get_position_by_id(candidate.position_id)
    team = team_repo.get_team_by_id(candidate.team_id)

    meeting_room = meeting_room_repo.get_room_by_id(data["meeting_room"])
    office = offices_repo.find(meeting_room.office_id)

    template = templates_repo.get_template_by_key(template_key)
    params = parameters_repo.get_by_params_name(template["params"])
    values = parameters_repo.get_key_value_by_params(params, candidate_id = result_interview.candidate_id, office_id = office.id, employee_code = employee)

    values["$NameInterviewer"] = user.fullname
    values["$PositionName"] = position.name
    values["$JobTitle"] = team.name
    if template_key in ["add_interview_schedule", "change_interview_schedule"]:
      values["$LocationName"] = office.name
      values["$InterviewRound"] = result_interview.type_kbn.value
      values["$MeetingRoomName"] = meeting_room.name
      flag_set_cv_file = True

    data_mail = {
      "values": values,
      "body": template["body"],
      "user": user,
      "template": template,
      "candidate": candidate,
      "office": office,
      "flag_set_cv_file": flag_set_cv_file,
    }

    return data_mail


  # Add interview detail
  # Params:
  #   @result_interview: Data interview
  #   @data: Data request
  # Output:
  #   return: Data mail
  def add_interview_detail(self, result_interview, data):
    with self.session_factory() as session:
      user_repo = UsersRepository(self.session_factory, self.session_factory_read)

      session.query(Interviews).filter(Interviews.id == result_interview.id).update({
        Interviews.meeting_room_id: data["meeting_room"],
        Interviews.time: data["time"],
        Interviews.date: data["date"],
        Interviews.updated_user: data["employee_code"],
      })

      data_interview_detail = {}
      list_mail = []
      list_interviewer = []

      for employee in data["employee"]:
        data_interview_detail = {
          "interview_id": result_interview.id,
          "employee_code": employee,
          "created_user": data["employee_code"]
        }

        data_interview_detail = InterviewDetails(**data_interview_detail)

        session.add(data_interview_detail)

        user = user_repo.get_user_by_employee_code(employee)

        data_mail = self.create_mail_interview(user, employee, data, result_interview, "add_interview_schedule")
        list_interviewer.append(user.fullname)

        list_mail.append(data_mail)

      session.commit()

      return {
        "list_mail": list_mail,
        "list_interviewer": list_interviewer
      }


  # Edit interview detail
  # Params:
  #   @result_interview: Data interview
  #   @data: Data request
  # Output:
  #   return: Void
  def edit_interview_detail(self, result_interview, data):
    with self.session_factory() as session:
      user_repo = UsersRepository(self.session_factory, self.session_factory_read)

      result_interview_detail = session.query(InterviewDetails).filter(InterviewDetails.interview_id == result_interview.id).all()

      list_mail = []
      list_new_interviewer = []

      if not data["flag_not_interview"]:
        session.query(Interviews).filter(Interviews.id == result_interview.id).update({
          Interviews.meeting_room_id: data["meeting_room"],
          Interviews.time: data["time"],
          Interviews.date: data["date"],
          Interviews.updated_user: data["employee_code"],
        })

        list_old_interviewer = []

        for interview_detail_item in result_interview_detail:
          list_old_interviewer.append(interview_detail_item.employee_code)
          session.query(InterviewDetails).filter(InterviewDetails.id == interview_detail_item.id).delete()

        # Employee not in list old interviewer will send cancel mail
        for old_interviewer in list_old_interviewer:
          if old_interviewer not in data["employee"]:
            user = user_repo.get_user_by_employee_code(old_interviewer)
            data_mail_cancel = self.create_mail_interview(user, old_interviewer, data, result_interview, "cancel_interview_schedule")

            list_mail.append(data_mail_cancel)

        for employee in data["employee"]:
          data_interview_detail = {
            "interview_id": result_interview.id,
            "employee_code": employee,
            "created_user": data["employee_code"],
          }

          data_interview_detail = InterviewDetails(**data_interview_detail)

          session.add(data_interview_detail)

          user = user_repo.get_user_by_employee_code(employee)

          # Change interview schedule mail
          data_mail_change = self.create_mail_interview(user, employee, data, result_interview, "change_interview_schedule")
          list_new_interviewer.append(user.fullname)

          list_mail.append(data_mail_change)

      else:
        result_candidate = session.query(Candidates).filter(Candidates.id == data["candidate_id"]).first()

        session.query(Candidates).filter(Candidates.id == data["candidate_id"]).update({
          Candidates.status: kbn.CandidateStatus.NOT_INTERVIEW.value,
          Candidates.previous_status: result_candidate.status.value,
          Candidates.updated_user: data["employee_code"]
        })

        session.query(Interviews).filter(Interviews.id == result_interview.id).update({
          Interviews.status: kbn.InterviewStatus.NOT_INTERVIEW.value,
          Interviews.updated_user: data["employee_code"],
        })

        for interview_detail_item in result_interview_detail:
          session.query(InterviewDetails).filter(InterviewDetails.id == interview_detail_item.id).update({
            InterviewDetails.evaluate: kbn.Evaluate.FAILED.value,
            InterviewDetails.updated_user: data["employee_code"],
          })

          user = user_repo.get_user_by_employee_code(interview_detail_item.employee_code)

          data_mail_cancel = self.create_mail_interview(user, interview_detail_item.employee_code, data, result_interview, "cancel_interview_schedule")

          list_mail.append(data_mail_cancel)

      session.commit()

      return {
        "list_mail": list_mail,
        "list_interviewer": list_new_interviewer
      }
