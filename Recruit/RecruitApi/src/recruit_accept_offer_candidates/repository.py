"""
Received offer candidates repository
"""

from core import CommonRepository, CommonException, ERR_MESSAGE
from core.message import MESSAGE
from models import Candidates, Positions, Teams, Offices, Mails
from helpers import kbn
from helpers.const import CODE, TOKEN_EXPIRED
from helpers import context
from sqlalchemy import literal, desc
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta

class AcceptOfferCandidatesRepository(CommonRepository):
  """
  Repository of Service offer candidates
  """


  # Get candidates
  # Output:
  #   return: Candidates list
  def get_list(self):
    with self.session_factory() as session:
      mails = session.query(Mails).filter(
        Mails.is_deleted == kbn.DeleteFlag.OFF.value,
        Mails.status == kbn.MailFlag.UNSENT.value
      ).subquery()

      positions = session.query(Positions).filter(Positions.is_deleted == kbn.DeleteFlag.OFF.value).subquery()
      teams = session.query(Teams).filter(Teams.is_deleted == kbn.DeleteFlag.OFF.value).subquery()

      candidates = session.query(
        Candidates.id, Candidates.fullname, Candidates.email, Candidates.cv_file_path,
        Candidates.telephone_no, Candidates.position_id, Candidates.team_id,
        Candidates.start_join_date, Candidates.gender,
        positions.c.name.label("position"), teams.c.name.label("team"),
        literal(MESSAGE.CANDIDATE_STATUS.ACCEPT_OFFER).label("status"), Offices.name.label("office"),
        mails.c.id.label("mail_id"), mails.c.title,
        mails.c.body, mails.c.attached_file, mails.c.carbon_copy, mails.c.attached_file_name,mails.c.id.label("mail_id")
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
        Candidates.status == kbn.CandidateStatus.ACCEPT_OFFER.value
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


  # Edit start join date
  # Param:
  #   @candidate_id: Candidate id
  #   @start_join_date: Start join date
  # Return: None
  def edit_start_join(self, candidate_id: int, start_join_date: str):
    with self.session_factory() as session:
      session.query(Candidates).filter(Candidates.id == candidate_id).update({
        Candidates.status: kbn.CandidateStatus.ACCEPT_OFFER.value,
        Candidates.start_join_date: start_join_date,
        Candidates.updated_user: context.user.value["employee_code"]
      })
      session.commit()


  # Get candidate by id
  # Param:
  #   @candidate_id: Candidate id
  # Return: Email
  def get_candidate_by_id(self, candidate_id: int) -> str:
    with self.session_factory() as session:
      candidates = session.query(Candidates.email, Candidates.status, Offices.id.label("office_id"), Offices.mail_admin, Offices.password_mail).filter(
        Candidates.id == candidate_id,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.status == kbn.CandidateStatus.ACCEPT_OFFER.value,
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).first()
      return jsonable_encoder(candidates)


  # Add token access form candidate
  # Param:
  #   @candidate_id: Candidate id
  #   @token: Token
  # Return: None
  def add_token(self, candidate_id: int, token: str):
    with self.session_factory() as session:
      data_update = {
        Candidates.updated_user: context.user.value["employee_code"]
      }

      if token == "":
        data_update.update({
          Candidates.expire: datetime.now() + timedelta(days=TOKEN_EXPIRED),
          Candidates.status: kbn.CandidateStatus.SEND_FORM.value,
          Candidates.previous_status: kbn.CandidateStatus.ACCEPT_OFFER.value,
        })
      else:
        data_update.update({
          Candidates.token: token,
          Candidates.expire: datetime.now() + timedelta(days=TOKEN_EXPIRED),
        })

      session.query(Candidates).filter(
        Candidates.id == candidate_id,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.status == kbn.CandidateStatus.ACCEPT_OFFER.value
      ).update(data_update)

      # Execute transaction
      session.commit()


  # Get candidate by token
  # Param:
  #   @token: Token
  # Return: Candidate
  def get_candidate_by_token(self, token: str):
    with self.session_factory() as session:
      candidate = session.query(Candidates).filter(
        Candidates.token == token,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.expire > datetime.now()
      ).first()

      if not candidate:
        raise CommonException(code=CODE.API.NOT_FOUND, message=ERR_MESSAGE.CANDIDATE_NOT_EXIST)

      candidate = jsonable_encoder(candidate)

      return candidate


  # Edit candidate by token
  # Param:
  #   @token: Token
  #   @candidate: Candidate
  # Return: None
  def edit_candidate_by_token(self, token: str, candidate: dict):
    with self.session_factory() as session:
      candidate["token"] = None
      candidate["expire"] = None
      candidate["status"] = kbn.CandidateStatus.UPDATED_FORM.value
      candidate["previous_status"] = kbn.CandidateStatus.SEND_FORM.value
      candidate = session.query(Candidates).filter(
        Candidates.token == token,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.expire > datetime.now()
      ).update(candidate)
      # Execute transaction
      session.commit()
