"""
Candidates pass list repository
"""

from core import CommonRepository
from models import Candidates, Positions, Teams, Offices, Mails, Users
from helpers import kbn
from helpers.common import bcrypt
from helpers.const import PASSWORD_DEFAULT
from sqlalchemy import desc
from fastapi.encoders import jsonable_encoder
from datetime import date

class CandidatesPassListRepository(CommonRepository):
  """
  Repository of Service candidate pass list
  """

  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      mails = session.query(Mails).filter(
        Mails.is_deleted == kbn.DeleteFlag.OFF.value,
        Mails.status == kbn.MailFlag.UNSENT.value
      ).subquery()
      data_candidates = jsonable_encoder(session.query(Candidates.id, Candidates.fullname,
        Teams.name.label("team"), Positions.name.label("position"),
        Candidates.email, Candidates.telephone_no, Candidates.full_address, Candidates.gender,
        Candidates.start_join_date, Candidates.birthday,  Offices.name.label("office"),
        mails.c.id.label("id_template"), mails.c.title,
        mails.c.body, mails.c.attached_file, mails.c.carbon_copy,
      ).outerjoin(
        mails, mails.c.candidate_id == Candidates.id
      ).outerjoin(
        Teams, Teams.id == Candidates.team_id
      ).outerjoin(
        Positions, Positions.id == Candidates.position_id
      ).outerjoin(
        Offices, Offices.id == Candidates.office_id
      ).filter(
        Candidates.status == kbn.CandidateStatus.TUTORIAL.value,
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Teams.is_deleted == kbn.DeleteFlag.OFF.value,
        Positions.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
      ).order_by(desc(Candidates.updated_date)).all())

      for candidate in data_candidates:
        if candidate["gender"] == kbn.Gender.MALE.value:
          candidate["gender"] = "Nam"
        elif candidate["gender"] == kbn.Gender.FEMALE.value:
          candidate["gender"] = "Nữ"
        else:
          candidate["gender"] = "Không xác định"

      return data_candidates


  # Get email of candidate by id candidate and email of office work
  # Params:
  #   @id_candidate: id of candidate
  # Output:
  #  return: email candidate and email of office
  def get_email(self, id_candidate):
    with self.session_factory_read() as session:
      return session.query(Candidates.email, Offices.mail_admin, Offices.password_mail).outerjoin(
        Offices, Candidates.office_id == Offices.id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.id == id_candidate
      ).first()


  # Update status mail when send mail for candidate and update status for candidate
  # Params:
  #   @list_id_candidate: list id of candidate
  # Output:
  #  return: None
  def update_status_mail(self, list_id_candidate):
    with self.session_factory() as session:
      count_candidate_all = session.query(Candidates).filter(Candidates.status == kbn.CandidateStatus.ALL_OK.value).count()
      number_year = int(str(date.today().year*100)[2:])
      session.query(Mails).filter(
        Mails.candidate_id.in_(list_id_candidate),
        Mails.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Mails.status: kbn.CandidateResultStatus.SENT.value,
        Mails.updated_user: "admin",
      })

      session.query(Candidates).filter(
        Candidates.id.in_(list_id_candidate),
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value
      ).update({
        Candidates.status: kbn.CandidateStatus.ALL_OK.value,
        Candidates.updated_user: "admin",
      })

      number_year = number_year + count_candidate_all

      # Get information of candidate add table user
      list_candidate = session.query(Candidates).filter(Candidates.id.in_(list_id_candidate)).all()
      # Add password default is "Test123@"
      for candidate in list_candidate:
        user = {
          "employee_code": "VN" + str(number_year),
          "password": bcrypt(PASSWORD_DEFAULT),
          "fullname": candidate.fullname,
          "email": candidate.email,
          "birthday": candidate.birthday,
          "full_address": candidate.full_address,
          "telephone_no": candidate.telephone_no,
          "position_id": candidate.position_id,
          "identification_number": candidate.identification_number,
          "place_issued_identification": candidate.place_issued_identification,
          "date_issued_identification": candidate.date_issued_identification,
          "office_id": candidate.office_id,
          "created_user": candidate.created_user,
          "created_date": candidate.created_date
        }

        number_year += 1
        # Add user
        session.add(Users(**user))
      session.commit()
