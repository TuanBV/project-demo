"""
Invite interview repository
"""

from core import CommonRepository
from models import Candidates, Positions, Teams, Offices, Interviews, Mails
from helpers import kbn
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc


class InviteInterviewRepository(CommonRepository):
  """
  Repository of Service invite interview
  """


  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      subquery_mails = session.query(Mails).filter(Mails.status == kbn.MailFlag.UNSENT.value, Mails.is_deleted == kbn.DeleteFlag.OFF.value).subquery()

      query_candidates = session.query(Candidates.id, Candidates.fullname, Teams.name.label("team"), Positions.name.label("position"), Candidates.email, Candidates.gender,
        Candidates.telephone_no, Candidates.status, Offices.name.label("office"), Interviews.time, Interviews.interview_form, subquery_mails.c.id.label("mail_id"),
        subquery_mails.c.title, subquery_mails.c.body, subquery_mails.c.attached_file, subquery_mails.c.carbon_copy, Interviews.date,
      ).join(
        Teams, Teams.id == Candidates.team_id
      ).join(
        Positions, Positions.id == Candidates.position_id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).join(
        Interviews, Interviews.candidate_id == Candidates.id
      ).outerjoin(
        subquery_mails, subquery_mails.c.candidate_id == Candidates.id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Teams.is_deleted == kbn.DeleteFlag.OFF.value,
        Positions.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
        Candidates.status.in_(
          [kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value,
          kbn.CandidateStatus.INVITE_SECOND_INTERVIEW.value,
          kbn.CandidateStatus.INVITE_TEST.value]),
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

      payload["item"] = data_candidates

      return payload


  # Get candidate by list id
  # Params:
  #   @list_id: List id of candidate
  # Output:
  #   return: List data candidate
  def get_by_list_id(self, list_id):
    with self.session_factory_read() as session:
      result_candidate = session.query(Candidates.id, Candidates.status, Candidates.position_id, Candidates.office_id, Interviews.interview_form
      ).outerjoin(
        Interviews, Interviews.candidate_id == Candidates.id
      ).filter(Candidates.id.in_(list_id), Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value).all()

      return result_candidate


  # Get list candidates send mail
  # Params:
  #   @list_mail_id: List id of mail
  # Output:
  #   return: Candidates list
  def get_list_send_mail(self, list_mail_id):
    with self.session_factory_read() as session:
      candidates = session.query(
        Candidates.id, Candidates.email, Candidates.status,
        Mails.title, Mails.body, Mails.carbon_copy, Mails.id.label("mail_id"), Offices.mail_admin, Offices.password_mail
      ).join(
        Candidates, Candidates.id == Mails.candidate_id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).filter(
        Candidates.id.in_(list_mail_id),
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        Mails.status == kbn.MailFlag.UNSENT.value,
      ).all()

      return jsonable_encoder(candidates)


  # Update candidate status
  # Params:
  #   @candidate_id: Candidate id
  # Output:
  #   return: Void
  def update_status(self, candidate_id, status, old_status, updater):
    with self.session_factory_read() as session:
      session.query(Candidates).filter(
        Candidates.id == candidate_id,
      ).update({
        Candidates.status: status,
        Candidates.previous_status: old_status,
        Candidates.updated_user: updater
      })

      session.commit()


  # Get mail not sent of candidate
  # Params:
  #   @list_id: List candidate id
  # Output:
  #   return: List mail
  def get_mail_not_sent(self, list_id):
    with self.session_factory_read() as session:
      result_mail_candidate = session.query(Mails).filter(Mails.candidate_id.in_(list_id), Mails.status == kbn.MailFlag.UNSENT.value).all()

      return result_mail_candidate
