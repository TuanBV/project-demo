"""
Candidates repository
"""

from core import CommonRepository
from models import Candidates, Recommenders, Positions, Teams, Offices, Mails
from copy import deepcopy
from helpers import kbn
from fastapi.encoders import jsonable_encoder
from setting import settings
from sqlalchemy import desc

class CandidatesRepository(CommonRepository):
  """
  Repository of Service candidate
  """

  # Add candidates
  # Param:
  #   @data: Data request
  # Output:
  #   return: Void
  def add(self, data):
    with self.session_factory() as session:
      data_candidate = deepcopy(data["candidate"])
      data_candidate["position_id"] = int(data_candidate["position_id"])
      data_candidate["team_id"] = int(data_candidate["team_id"])
      data_candidate["office_id"] = int(data_candidate["office_id"])
      data_candidate["recommender_id"] = int(data_candidate["recommender_id"]) if data_candidate["recommender_id"] else None

      data_candidate = Candidates(**data_candidate)

      session.add(data_candidate)

      data_candidate = data_candidate.__dict__

      # Execute transaction
      session.commit()

      return data_candidate


  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}

      query_candidates = session.query(Candidates.id, Candidates.fullname, Teams.name.label("team"), Positions.name.label("position"), Candidates.email,
        Candidates.telephone_no, Candidates.status, Candidates.application_date, Candidates.cv_file_path, Candidates.previous_status,
        Recommenders.fullname.label("recommender"), Offices.name.label("office")
      ).join(
        Recommenders, Recommenders.id == Candidates.recommender_id
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
        Recommenders.is_deleted == kbn.DeleteFlag.OFF.value,
        Candidates.status == kbn.CandidateStatus.RECEIVE_CV.value,
      ).order_by(desc(Candidates.created_date))

      # Get count data filter
      data_candidates = jsonable_encoder(query_candidates.all())

      for candidate in data_candidates:
        candidate["cv_file_path"] = f'{settings.DOMAIN_FILE}/{candidate["cv_file_path"]}'

      payload["item"] = data_candidates

      return payload


  # Get candidate
  # Params:
  #   @candidate_id: Candidate id
  # Output:
  #   return: Data candidate
  def get_candidate_by_id(self, candidate_id):
    with self.session_factory_read() as session:
      result_candidate = session.query(Candidates.id, Candidates.date_issued_identification, Candidates.telephone_no, Candidates.status, Candidates.fullname,
        Candidates.bank_account, Candidates.application_date, Candidates.previous_status, Candidates.email, Candidates.team_id, Candidates.position_id,
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


  # Edit candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def edit(self, data):
    with self.session_factory() as session:
      data_candidate = deepcopy(data["candidate"])

      data_candidate["updated_user"] = data["employee_code"]

      session.query(Candidates).filter(Candidates.id == data["candidate_id"]).update(data_candidate)

      # Execute transaction
      session.commit()


  # Delete candidate
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def delete(self, data):
    with self.session_factory() as session:
      session.query(Candidates).filter(Candidates.id == data["candidate_id"]).update({
        Candidates.is_deleted: kbn.DeleteFlag.ON.value,
        Candidates.updated_user: data["employee_code"]
      })

      # Execute transaction
      session.commit()


  # Get candidate by list id
  # Params:
  #   @list_id: List id of candidate
  # Output:
  #   return: List data candidate
  def get_list_candidate_by_list_id(self, list_id):
    with self.session_factory_read() as session:
      result_candidate = session.query(Candidates).filter(Candidates.id.in_(list_id)).all()

      return result_candidate


  # Get candidate and mail by list id
  # Params:
  #   @list_id: List id of candidate
  # Output:
  #   return: List candidate and mail
  def get_list_candidate_and_mail_by_list_id(self, list_id):
    with self.session_factory_read() as session:
      mails = session.query(Mails).filter(
        Mails.status == kbn.MailFlag.UNSENT.value,
        Mails.is_deleted == kbn.DeleteFlag.OFF.value).subquery()

      result_candidate = session.query(Candidates.id, Candidates.status, Candidates.position_id, Candidates.office_id, mails.c.id.label("mail_id")).outerjoin(
        mails, mails.c.candidate_id == Candidates.id,
      ).filter(Candidates.id.in_(list_id)).all()

      return result_candidate


  # Edit status list candidate
  # Params:
  #   @list_data: List candidate
  #   @status: New status
  #   @updated_user: User updated
  # Output:
  #   return: Void
  def edit_status_list_candidate(self, list_data, status, updated_user):
    with self.session_factory() as session:
      add_count_apply = 0
      if status.value in [kbn.CandidateStatus.FAILED_CV.value, kbn.CandidateStatus.FAILED_TEST.value,
          kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value, kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value,
          kbn.CandidateStatus.REFUSE_OFFER.value, kbn.CandidateStatus.NOT_INTERVIEW.value]:
        add_count_apply = 1

      for candidate in list_data:
        session.query(Candidates).filter(Candidates.id == candidate.id).update({
          Candidates.status: status.value,
          Candidates.previous_status: candidate.status.value,
          Candidates.count_apply: candidate.count_apply + add_count_apply,
          Candidates.updated_user: updated_user,
        })

      session.commit()
