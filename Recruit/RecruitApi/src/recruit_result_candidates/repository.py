"""
Candidates repository
"""

from core import CommonRepository
from core.message import MESSAGE
from models import Candidates, Positions, Teams, Mails, Offices
from helpers import kbn, context
from helpers.const import NUMBER_EXPERIENCES
from sqlalchemy import and_, or_, case
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc


class ResultCandidatesRepository(CommonRepository):
  """
  Repository of Service result candidate
  """


  # Get interviewed candidates
  # Output:
  #   return: Candidates list
  def get_interviewed_candidates(self, option_value):
    with self.session_factory() as session:
      mails = session.query(Mails).filter(
        Mails.is_deleted == kbn.DeleteFlag.OFF.value,
        Mails.status == kbn.MailFlag.UNSENT.value
      ).subquery()

      positions = session.query(Positions).filter(Positions.is_deleted == kbn.DeleteFlag.OFF.value).subquery()
      teams = session.query(Teams).filter(Teams.is_deleted == kbn.DeleteFlag.OFF.value).subquery()

      if option_value == 1:
        filter_list = or_(
          Candidates.status == kbn.CandidateStatus.FAILED_TEST.value,
          Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value,
          Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value,
        )
      elif option_value == 2:
        filter_list = or_(
          and_(
            Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.number_experiences > NUMBER_EXPERIENCES,
            positions.c.id == kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.team_id != kbn.Team.TESTER.value,
            Candidates.number_experiences <= NUMBER_EXPERIENCES,
            positions.c.id == kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.team_id == kbn.Team.TESTER.value,
            positions.c.id == kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            positions.c.id != kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.position_id != kbn.Positions.LEADER.value,
            Candidates.office_id == kbn.Office.HUE.value,
            Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value
          ),
          and_(
            Candidates.position_id == kbn.Positions.LEADER.value,
            Candidates.office_id == kbn.Office.HUE.value,
            Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value
          ),
        )
      else:
        filter_list = or_(
          Candidates.status == kbn.CandidateStatus.FAILED_TEST.value,
          Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value,
          Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value,
          and_(
            Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.number_experiences > NUMBER_EXPERIENCES,
            positions.c.id == kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.team_id != kbn.Team.TESTER.value,
            Candidates.number_experiences <= NUMBER_EXPERIENCES,
            positions.c.id == kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.team_id == kbn.Team.TESTER.value,
            positions.c.id == kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            positions.c.id != kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.position_id != kbn.Positions.LEADER.value,
            Candidates.office_id == kbn.Office.HUE.value,
            Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value
          ),
          and_(
            Candidates.position_id == kbn.Positions.LEADER.value,
            Candidates.office_id == kbn.Office.HUE.value,
            Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value
          ),
        )

      # Get status name by status code
      status = case(
        (Candidates.status == kbn.CandidateStatus.FAILED_TEST.value, MESSAGE.CANDIDATE_STATUS.FAILED_TEST),
        (Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value, MESSAGE.CANDIDATE_STATUS.FIRST_INTERVIEW_FAILED),
        (Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value, MESSAGE.CANDIDATE_STATUS.SECOND_INTERVIEW_FAILED),
        (Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value, MESSAGE.CANDIDATE_STATUS.FIRST_INTERVIEW_PASS),
        else_=MESSAGE.CANDIDATE_STATUS.SECOND_INTERVIEW_PASS,
      ).label("status")

      candidates = session.query(
        Candidates.id, Candidates.fullname, Candidates.email,
        Candidates.telephone_no, Candidates.position_id, Candidates.gender,
        status,
        mails.c.id.label("mail_id"), mails.c.title,
        mails.c.body, mails.c.attached_file, mails.c.carbon_copy, mails.c.attached_file_name,
        positions.c.id.label("position_id"), positions.c.name.label("position"),
        teams.c.id.label("team_id"), teams.c.name.label("team"), Offices.name.label("office")
      ).outerjoin(
        mails, mails.c.candidate_id == Candidates.id
      ).join(
        positions, positions.c.id == Candidates.position_id
      ).join(
        teams, teams.c.id == Candidates.team_id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.result_status == kbn.CandidateResultStatus.UNSENT.value,
        filter_list,
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


  # Get candidates by id
  # Params:
  #   @candidates_id: Candidates id
  # Output:
  #   return: Candidates list
  def get_candidates_by_id(self, candidates_id: list):
    with self.session_factory() as session:
      candidates = session.query(
        Candidates.id, Candidates.email, Candidates.status,
        Mails.title, Mails.body, Mails.carbon_copy,
        Mails.id.label("mail_id"), Mails.attached_file, Mails.attached_file_name,
        Offices.mail_admin, Offices.password_mail
      ).join(
        Mails, Mails.candidate_id == Candidates.id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).filter(
        Candidates.id.in_(candidates_id),
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Mails.is_deleted == kbn.DeleteFlag.OFF.value,
        Mails.status == kbn.MailFlag.UNSENT.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
      ).all()

      return jsonable_encoder(candidates)


  # Update result status candidate
  # Params:
  #   @candidate: candidate
  # Output:
  #   return: None
  def update_result_status(self, candidate):
    with self.session_factory() as session:
      interview_failed = [kbn.CandidateStatus.FAILED_TEST.value, kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value, kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value]
      result_candidate = session.query(Candidates).filter(Candidates.id == candidate["id"], Candidates.is_deleted == kbn.DeleteFlag.OFF.value).first()
      if candidate["status"] not in interview_failed:
        session.query(Candidates).filter(
          Candidates.id == candidate["id"],
          Candidates.result_status == kbn.CandidateResultStatus.UNSENT.value
        ).update({
          Candidates.status: kbn.CandidateStatus.SEND_OFFER.value,
          Candidates.previous_status: result_candidate.status.value,
          Candidates.updated_user: context.user.value["employee_code"]
        })
        session.commit()
      else:
        session.query(Candidates).filter(
          Candidates.id == candidate["id"],
          Candidates.result_status == kbn.CandidateResultStatus.UNSENT.value
        ).update({
          Candidates.result_status: kbn.CandidateResultStatus.SENT.value,
          Candidates.updated_user: context.user.value["employee_code"]
        })
        session.commit()
