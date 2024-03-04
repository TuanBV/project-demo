"""
Definition Containers
"""

from dependency_injector import containers, providers
from db.database import Database
from helpers.kbn import TYPE_DB
from recruit_users import UsersRepository, UsersService
from recruit_recommenders import RecommendersRepository, RecommendersService
from recruit_candidates import CandidatesRepository, CandidatesService
from recruit_candidates_confirm import CandidatesConfirmService, CandidatesConfirmRepository
from recruit_candidates_list import CandidatesListService, CandidatesListRepository
from recruit_positions import PositionsRepository, PositionsService
from recruit_teams import TeamsRepository, TeamsService
from recruit_templates import TemplatesRepository, TemplatesService
from recruit_parameters import ParametersService, ParametersRepository
from recruit_offices import OfficesService, OfficesRepository
from recruit_add_cv import AddCvService, AddCvRepository
from recruit_contact_candidate import ContactCandidateService, ContactCandidateRepository
from recruit_mails import MailService, MailRepository
from recruit_result_candidates import ResultCandidatesService, ResultCandidatesRepository
from recruit_candidates_pass_list import CandidatesPassListService, CandidatesPassListRepository
from recruit_offer_candidates import OfferCandidatesService, OfferCandidatesRepository
from recruit_invite_interview import InviteInterviewService, InviteInterviewRepository
from recruit_accept_offer_candidates import AcceptOfferCandidatesService, AcceptOfferCandidatesRepository
from recruit_confirm_test import ConfirmTestService, ConfirmTestRepository
from recruit_interview_schedule import InterviewScheduleService, InterviewScheduleRepository
from recruit_meeting_rooms import MeetingRoomsService, MeetingRoomsRepository
from recruit_black_list import BlackListRepository, BlackListService
from recruit_candidate_assessment import CandidateAssessmentRepository, CandidateAssessmentService
from recruit_staff_list import StaffListRepository, StaffListService
from core.logger import get_logger

class Container(containers.DeclarativeContainer):
  """
  Class Containers
  """
  wiring_config = containers.WiringConfiguration(modules=["routers"])
  config = providers.Configuration()

  logger = providers.Resource(get_logger)

  db = providers.Singleton(Database, db_kbn=TYPE_DB.WRITE)
  db_read = providers.Singleton(Database, db_kbn=TYPE_DB.READ)

  # repository
  users_repository = providers.Factory(UsersRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  recommenders_repository = providers.Factory(RecommendersRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  candidates_repository = providers.Factory(CandidatesRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  candidates_confirm_repository = providers.Factory(CandidatesConfirmRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  candidates_list_repository = providers.Factory(CandidatesListRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  staff_list_repository = providers.Factory(StaffListRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  candidates_pass_list_repository = providers.Factory(CandidatesPassListRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  positions_repository = providers.Factory(PositionsRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  teams_repository = providers.Factory(TeamsRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  templates_repository = providers.Factory(TemplatesRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  parameters_repository = providers.Factory(ParametersRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  offices_repository = providers.Factory(OfficesRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  add_cv_repository = providers.Factory(AddCvRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  contact_candidate_repository = providers.Factory(ContactCandidateRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  mails_repository = providers.Factory(MailRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  result_candidates_repository = providers.Factory(ResultCandidatesRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  offer_candidates_repository = providers.Factory(OfferCandidatesRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  invite_interview_repository = providers.Factory(InviteInterviewRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  accept_offer_candidates_repository = providers.Factory(AcceptOfferCandidatesRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  confirm_test_repository = providers.Factory(ConfirmTestRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  interview_schedule_repository = providers.Factory(InterviewScheduleRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  meeting_rooms_repository = providers.Factory(MeetingRoomsRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  black_list_repository = providers.Factory(BlackListRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)
  candidate_assessment_repository = providers.Factory(CandidateAssessmentRepository, session_factory=db.provided.session, session_factory_read=db_read.provided.session)

  # service
  recommenders_service = providers.Factory(RecommendersService, recommenders_repository=recommenders_repository)
  candidates_service = providers.Factory(CandidatesService, candidates_repository=candidates_repository)
  candidates_confirm_service = providers.Factory(CandidatesConfirmService, candidates_confirm_repository=candidates_confirm_repository)
  candidates_list_service = providers.Factory(CandidatesListService, candidates_list_repository=candidates_list_repository)
  staff_list_service = providers.Factory(StaffListService, staff_list_repository=staff_list_repository)
  candidates_pass_list_service = providers.Factory(
    CandidatesPassListService,
    candidates_pass_list_repository=candidates_pass_list_repository,
    mails_repository=mails_repository,
    templates_repository=templates_repository,
    parameters_repository=parameters_repository
  )
  positions_service = providers.Factory(PositionsService, positions_repository=positions_repository)
  teams_service = providers.Factory(TeamsService, teams_repository=teams_repository)
  users_service = providers.Factory(
    UsersService,
    users_repository=users_repository,
    mails_repository=mails_repository,
    templates_repository=templates_repository,
    parameters_repository=parameters_repository,
    offices_repository=offices_repository
  )
  templates_service = providers.Factory(TemplatesService, templates_repository=templates_repository)
  parameters_service = providers.Factory(ParametersService, parameters_repository=parameters_repository)
  offices_service = providers.Factory(OfficesService, offices_repository=offices_repository)
  add_cv_service = providers.Factory(AddCvService, add_cv_repository=add_cv_repository)
  contact_candidate_service = providers.Factory(ContactCandidateService, contact_candidate_repository=contact_candidate_repository)
  mails_service = providers.Factory(MailService, mails_repository=mails_repository)
  result_candidates_service = providers.Factory(
    ResultCandidatesService,
    result_candidates_repository=result_candidates_repository,
    candidates_repository=candidates_repository,
    mails_repository=mails_repository,
    templates_repository=templates_repository,
    parameters_repository=parameters_repository
  )
  offer_candidates_service = providers.Factory(OfferCandidatesService, offer_candidates_repository=offer_candidates_repository)
  invite_interview_service = providers.Factory(InviteInterviewService, invite_interview_repository=invite_interview_repository,
    mails_repository=mails_repository, templates_repository=templates_repository, parameters_repository=parameters_repository)
  accept_offer_candidates_service = providers.Factory(
    AcceptOfferCandidatesService,
    mails_repository=mails_repository,
    templates_repository=templates_repository,
    parameters_repository=parameters_repository,
    accept_offer_candidates_repository=accept_offer_candidates_repository,
    candidates_repository=candidates_repository,
    result_candidates_repository= result_candidates_repository)
  confirm_test_service = providers.Factory(ConfirmTestService, confirm_test_repository=confirm_test_repository)
  interview_schedule_service = providers.Factory(InterviewScheduleService, interview_schedule_repository=interview_schedule_repository)
  meeting_rooms_service = providers.Factory(MeetingRoomsService, meeting_rooms_repository=meeting_rooms_repository)
  black_list_service = providers.Factory(BlackListService,
    black_list_repository=black_list_repository,
    candidates_list_repository=candidates_list_repository
  )
  candidate_assessment_service = providers.Factory(CandidateAssessmentService, candidate_assessment_repository=candidate_assessment_repository)
