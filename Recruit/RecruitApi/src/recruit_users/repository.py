"""
User repository
"""

from core import CommonRepository, CommonException, ERR_MESSAGE
from models import Users, Positions, Offices, Candidates, Interviews
from helpers import kbn
from helpers.const import PASSWORD_DEFAULT, NUMBER_EXPERIENCES
from helpers.common import bcrypt, checkpw
from helpers import context
from datetime import datetime
from sqlalchemy import func, and_, or_

class UsersRepository(CommonRepository):
  """
  Repository of user
  """


  # Get user by email
  # Params:
  #   @email: User email
  # Output:
  #   return: Data user
  def get_user_data(self, email = ""):
    with self.session_factory_read() as session:
      query_user_data = session.query(
        Users.email, Users.fullname, Users.office_id, Users.employee_code, Users.password, Users.position_id, Users.login_failed_count, Users.office_id
      ).filter(Users.is_deleted == kbn.DeleteFlag.OFF.value)

      if email:
        result = query_user_data.filter(Users.email == email).first()
      else:
        user = context.user.value
        result = query_user_data.filter(Users.employee_code == user["employee_code"]).first()

      return result


  # Count record of page
  # Params:
  # office_id: id of office
  # Output:
  #   return: Data count record
  def count_record(self, office_id):
    with self.session_factory_read() as session:
      # Query count
      query_count = session.query(func.count(Candidates.id).label("count")).filter(Candidates.is_deleted == kbn.DeleteFlag.OFF.value, Candidates.office_id == office_id)

      # Count record of add cv
      add_cv = query_count.filter(Candidates.status == kbn.CandidateStatus.RECEIVE_CV.value, Candidates.office_id == office_id).first()

      # Count record of contact confirm
      contact_candidate = query_count.filter(
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
        ),
        Candidates.office_id == office_id
      ).first()

      # Count record of confirm test
      confirm_test = query_count.join(
        Interviews, Interviews.candidate_id == Candidates.id
      ).filter(
        Candidates.status == kbn.CandidateStatus.TEST.value,
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
        Interviews.type_kbn == kbn.InterviewType.TEST.value,
        Candidates.office_id == office_id,
      ).first()

      # Count record of invite interview
      invite_interview = query_count.filter(
        Candidates.status.in_(
          [kbn.CandidateStatus.INVITE_FIRST_INTERVIEW.value,
          kbn.CandidateStatus.INVITE_SECOND_INTERVIEW.value,
          kbn.CandidateStatus.INVITE_TEST.value]),
          Candidates.office_id == office_id
      ).first()

      # Count record of interview schedule
      interview_schedule = query_count.join(
        Interviews, Interviews.candidate_id == Candidates.id
      ).filter(
        Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
        Interviews.type_kbn.in_([kbn.InterviewType.FIRST_INTERVIEW.value, kbn.InterviewType.SECOND_INTERVIEW.value]),
        Candidates.status.in_([kbn.CandidateStatus.FIRST_INTERVIEW.value, kbn.CandidateStatus.SECOND_INTERVIEW.value]),
        Candidates.office_id == office_id
      ).first()

      # Count record of candidate assessment
      candidate_assessment = query_count.join(
        Interviews, Interviews.candidate_id == Candidates.id
      ).filter(Interviews.status == kbn.InterviewStatus.PREPARE_INTERVIEW.value,
        Interviews.type_kbn.in_([kbn.InterviewType.FIRST_INTERVIEW.value, kbn.InterviewType.SECOND_INTERVIEW.value]),
        Interviews.meeting_room_id.is_not(None),
        Candidates.status.in_(
          [kbn.CandidateStatus.FIRST_INTERVIEW.value,
          kbn.CandidateStatus.SECOND_INTERVIEW.value]
        ),
        Candidates.office_id == office_id
      ).first()

      # Count record of send_results
      send_results = query_count.outerjoin(
        Positions, Candidates.position_id == Positions.id
      ).filter(
        or_(
          Candidates.status == kbn.CandidateStatus.FAILED_TEST.value,
          Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_FAILED.value,
          Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_FAILED.value,
          and_(
            Candidates.status == kbn.CandidateStatus.SECOND_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.number_experiences > NUMBER_EXPERIENCES,
            Positions.id == kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Candidates.number_experiences <= NUMBER_EXPERIENCES,
            Positions.id == kbn.Positions.STAFF.value
          ),
          and_(
            Candidates.status == kbn.CandidateStatus.FIRST_INTERVIEW_PASS.value,
            Candidates.office_id != kbn.Office.HUE.value,
            Positions.id != kbn.Positions.STAFF.value
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
        ),
        Candidates.result_status == kbn.CandidateResultStatus.UNSENT.value,
        Candidates.office_id == office_id
      ).first()

      # Count record of update offers
      update_offers = query_count.filter(Candidates.status == kbn.CandidateStatus.SEND_OFFER.value, Candidates.office_id == office_id).first()

      # Count record of update offers
      send_forms = query_count.filter(Candidates.status == kbn.CandidateStatus.ACCEPT_OFFER.value, Candidates.office_id == office_id).first()

      # Count record of candidate confirm
      candidate_confirm = query_count.filter(
        Candidates.status.in_([kbn.CandidateStatus.UPDATED_FORM.value, kbn.CandidateStatus.SEND_FORM.value]),
        Candidates.office_id == office_id
      ).first()

      # Count record of candidate pass confirm
      candidate_pass_list = query_count.filter(Candidates.status == kbn.CandidateStatus.TUTORIAL.value, Candidates.office_id == office_id).first()

    return {
      "add_cv": add_cv.count,
      "contact_candidate": contact_candidate.count,
      "confirm_test": confirm_test.count,
      "invite_interview": invite_interview.count,
      "interview_schedule": interview_schedule.count,
      "candidate_assessment": candidate_assessment.count,
      "send_results": send_results.count,
      "update_offers": update_offers.count,
      "send_forms": send_forms.count,
      "candidate_confirm": candidate_confirm.count,
      "candidate_pass_list": candidate_pass_list.count,
    }

  # Get list user
  # Params:
  # Output:
  #   return: Data user
  def get_list(self):
    with self.session_factory_read() as session:
      query = session.query(Users.employee_code, Users.fullname, Users.email, Users.full_address,
        Users.telephone_no, Offices.name.label("office"), Positions.name.label("position"), Users.gender
      ).outerjoin(
        Positions, Users.position_id == Positions.id
      ).outerjoin(
        Offices, Users.office_id == Offices.id
      ).filter(Users.is_deleted == kbn.DeleteFlag.OFF.value)

      return query.all()


  # Add user
  # Params:
  #   @data_user
  # Output:
  #   return: Data user
  def add(self, data_user):
    with self.session_factory() as session:
      # Add password default is "Test123@"
      data_user["password"] = bcrypt(PASSWORD_DEFAULT)

      # Add user
      session.add(Users(**data_user))
      session.commit()


  # Edit user
  # Params:
  #   @data_user: data request
  #   @employee_code: employee code of user
  # Output: Nones
  def edit(self, employee_code, data_user):
    with self.session_factory() as session:
      # Update user
      session.query(Users).filter(Users.employee_code == employee_code).update(data_user)
      session.commit()


  # Delete user
  # Params:
  #   @employee_code: employee code of user
  # Output: None
  def delete(self, employee_code):
    with self.session_factory() as session:
      # Delete user
      session.query(Users).filter(Users.employee_code == employee_code).update({
        Users.is_deleted: kbn.DeleteFlag.ON.value,
      })
      session.commit()


  # Get user by employee code
  # Params:
  #   @employee_code: employee code of user
  # Output: user
  def get_user_by_employee_code(self, employee_code):
    with self.session_factory_read() as session:
      return session.query(Users).filter(Users.employee_code == employee_code, Users.is_deleted == kbn.DeleteFlag.OFF.value).first()


  # Check employee code of user
  # Params:
  #   @employee_code: code of employee
  # Output:
  #   return: boolean
  def check_employee_code(self, employee_code):
    with self.session_factory_read() as session:
      user = session.query(Users.employee_code).filter(Users.employee_code == employee_code).first()
      # If employee_code exist
      if user:
        return False
      return True


  # Check email of user
  # Params:
  #   @email: mail of user
  #   @employee_code: code of user
  # Output:
  #   return: boolean
  def check_email(self, email, employee_code=None):
    with self.session_factory_read() as session:
      user = session.query(Users.email, Users.employee_code).filter(Users.email == email).first()
      # Email not register
      if not user or (employee_code and user.employee_code == employee_code):
        return True
      return False


  # Check identification number of user
  # Params:
  #   @identification_number: identification number of user
  #   @employee_code: code of user
  # Output:
  #   return: boolean
  def check_identification_number(self, identification_number, employee_code=None):
    with self.session_factory_read() as session:
      user = session.query(Users.identification_number, Users.employee_code).filter(Users.identification_number == identification_number).first()
      # Email not register
      if (user and user.employee_code == employee_code) or not user:
        return True
      return False


  # Handle change password
  # Params:
  #   @data: Data
  # Output:
  #   return: None
  def change_password(self, data: dict):
    with self.session_factory_read() as session:
      user_conext = context.user.value
      user = session.query(Users).filter(
        Users.employee_code == user_conext["employee_code"]
      ).first()

      if checkpw(data["password"].strip(), user.password):
        session.query(Users).filter(
          Users.employee_code == user_conext["employee_code"]
        ).update({
          Users.password: bcrypt(data["new_password"])
        })
        session.commit()
      else:
        raise CommonException(message=ERR_MESSAGE.INCORRECT_PASSWORD)


  # Get user by token
  # Params:
  #   @token: Token
  # Output:
  #   return: User
  def get_user_by_token(self, token: str):
    with self.session_factory_read() as session:
      return session.query(Users).filter(
        Users.token == token,
        Users.is_deleted == kbn.DeleteFlag.OFF.value,
        Users.expire > datetime.now()
      ).first()


  # Get list interviewer
  # Params: None
  # Output:
  #   return: List data interviewer
  def get_list_interviewer(self):
    with self.session_factory_read() as session:
      return session.query(Users.employee_code, Users.fullname).filter(Users.is_deleted == kbn.DeleteFlag.OFF.value,
          Users.position_id.in_([kbn.Positions.LEADER.value, kbn.Positions.ADMIN.value, kbn.Positions.MANAGER.value])).all()


  # Update login failed count
  # Params: None
  # Output:
  #   return: List data interviewer
  def update_login_failed_count(self, email, login_failed_count):
    with self.session_factory() as session:
      # Update login failed count
      session.query(Users).filter(Users.email == email).update({
        Users.login_failed_count: login_failed_count,
      })
      session.commit()
