"""
Contact candidate repository
"""

from core import CommonRepository, CommonException, ERR_MESSAGE
from models import Candidates, Positions, Teams, Offices, Interviews
from helpers import kbn
from helpers.const import NUMBER_EXPERIENCES
from fastapi.encoders import jsonable_encoder
from setting import settings
from sqlalchemy import desc
from sqlalchemy import or_, and_


class ContactCandidateRepository(CommonRepository):
  """
  Repository of Service contact candidate
  """

  # Get list candidates
  # Params: None
  # Output:
  #  return: List candidates
  def get_list(self):
    with self.session_factory_read() as session:
      payload = {}
      interview_subquery = session.query(Interviews).filter(Interviews.is_deleted == kbn.DeleteFlag.OFF.value, Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value
      ).subquery()

      query_candidates = session.query(Candidates.id, Candidates.fullname, Teams.name.label("team"), Positions.name.label("position"), Candidates.email,
        Candidates.gender, Candidates.telephone_no, Candidates.status, Candidates.cv_file_path, Offices.name.label("office"), interview_subquery.c.note,
      ).join(
        Teams, Teams.id == Candidates.team_id
      ).join(
        Positions, Positions.id == Candidates.position_id
      ).join(
        Offices, Offices.id == Candidates.office_id
      ).outerjoin(
        interview_subquery, interview_subquery.c.candidate_id == Candidates.id
      ).filter(
        Candidates.is_deleted == kbn.DeleteFlag.OFF.value,
        Teams.is_deleted == kbn.DeleteFlag.OFF.value,
        Positions.is_deleted == kbn.DeleteFlag.OFF.value,
        Offices.is_deleted == kbn.DeleteFlag.OFF.value,
        or_(
          and_(
            Candidates.position_id == kbn.Positions.INTERNSHIP.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.status.in_([
              kbn.CandidateStatus.ACCEPT_CV.value,
              kbn.CandidateStatus.TEST_OK.value,
            ]),
          ),
          and_(
            Candidates.position_id.not_in([kbn.Positions.STAFF.value, kbn.Positions.INTERNSHIP.value]),
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.status == kbn.CandidateStatus.ACCEPT_CV.value
          ),
          and_(
            Candidates.position_id == kbn.Positions.STAFF.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.number_experiences <= NUMBER_EXPERIENCES,
            Candidates.status.in_([
              kbn.CandidateStatus.ACCEPT_CV.value
            ]),
          ),
          and_(
            Candidates.position_id == kbn.Positions.STAFF.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.number_experiences > NUMBER_EXPERIENCES,
            Candidates.status.in_([
              kbn.CandidateStatus.ACCEPT_CV.value,
              kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            ]),
          ),
          and_(
            Candidates.position_id == kbn.Positions.STAFF.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.team_id == kbn.Team.TESTER.value,
            Candidates.status.in_([
              kbn.CandidateStatus.ACCEPT_CV.value,
              kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            ]),
          ),
          and_(
            Candidates.position_id != kbn.Positions.LEADER.value,
            Candidates.office_id == kbn.Office.HUE.value,
            Candidates.status.in_([
              kbn.CandidateStatus.ACCEPT_CV.value
            ]),
          ),
          and_(
            Candidates.position_id == kbn.Positions.LEADER.value,
            Candidates.office_id == kbn.Office.HUE.value,
            Candidates.status.in_([
              kbn.CandidateStatus.ACCEPT_CV.value,
              kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            ]),
          ),
        )
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

      payload["item"] = data_candidates

      return payload


  # Add contact
  # Params:
  #   @data: Data request
  # Output:
  #   return: Void
  def add(self, data, data_candidate):
    with self.session_factory() as session:
      data["candidate"]["office_id"] = int(data["candidate"]["office_id"])

      flag_candidate_have_contact = session.query(Interviews).filter(
            Interviews.candidate_id == data_candidate.id,
            Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
            Interviews.is_deleted == kbn.DeleteFlag.OFF.value).first()

      if flag_candidate_have_contact:
        raise CommonException(message=ERR_MESSAGE.CANDIDATE_HAVE_CONTACT)

      # Check position to set new candidate status and interview status
      if (data_candidate.position_id == kbn.Positions.INTERNSHIP.value and
          data_candidate.team_id not in [kbn.Team.ADMIN.value, kbn.Team.COMTOR.value, kbn.Team.TESTER.value]):
        new_status = kbn.CandidateStatus.INVITE_TEST.value
        interview_type = kbn.InterviewType.TEST.value
      else:
        new_status = kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value
        interview_type = kbn.InterviewType.FIRST_INTERVIEW.value

      # Check candidate status to set new candidate status and itnerview
      if data_candidate.status == kbn.CandidateStatus.TEST_OK.value:
        new_status = kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value
        interview_type = kbn.InterviewType.FIRST_INTERVIEW.value
      elif data_candidate.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value:
        new_status = kbn.CandidateStatus.INVITE_SECOND_INTERVIEW.value
        interview_type = kbn.InterviewType.SECOND_INTERVIEW.value

      session.query(Candidates).filter(Candidates.id == int(data["candidate"]["candidate_id"])).update({
        Candidates.office_id: data["candidate"]["office_id"],
        Candidates.status: new_status,
        Candidates.previous_status: data_candidate.status.value,
        Candidates.updated_user: data["employee_code"],
      })

      data["candidate"]["created_user"] = data["employee_code"]

      del data["candidate"]["office_id"]

      data["candidate"]["type_kbn"] = interview_type
      data["candidate"]["interview_form"] = int(data["candidate"]["interview_form"])

      data_contact = Interviews(**data["candidate"])

      session.add(data_contact)

      # Execute transaction
      session.commit()
