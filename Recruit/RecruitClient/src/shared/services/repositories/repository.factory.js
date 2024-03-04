import UserRepository from 'services/repositories/restful/user.repository';
import RecommenderRepository from 'services/repositories/restful/recommender.repository';
import TemplateRepository from 'services/repositories/restful/template.repository';
import ParameterRepository from 'services/repositories/restful/parameter.repository';
import PositionRepository from 'services/repositories/restful/position.repository';
import CandidateRepository from 'services/repositories/restful/candidate.repository';
import CandidateConfirmRepository from 'services/repositories/restful/candidate-confirm.repository';
import TeamRepository from 'services/repositories/restful/team.repository';
import AddCvRepository from 'services/repositories/restful/add-cv.repository';
import ContactCandidateRepository from 'services/repositories/restful/contact-candidate.repository';
import MailRepository from 'services/repositories/restful/mail.repository';
import OfficeRepository from 'services/repositories/restful/office.repository';
import CandidateListRepository from 'services/repositories/restful/candidate-list.repository';
import BlackListRepository from 'services/repositories/restful/black-list.repository';
import CandidatePassListRepository from 'services/repositories/restful/candidate-pass-list.repository';
import InviteInterviewRepository from 'services/repositories/restful/invite-interview.repository';
import ConfirmTestRepository from 'services/repositories/restful/confirm-test.repository';
import InterviewScheduleRepository from 'services/repositories/restful/interview-schedule.repository';
import MeetingRoomRepository from 'services/repositories/restful/meeting-room.repository';
import CandidateAssessmentRepository from 'services/repositories/restful/candidate-assessment.repository';
import StaffListRepository from 'services/repositories/restful/staff-list.repository';

class RepositoryFactory {
  getRepository(serviceName) {
    switch (serviceName) {
      case 'user':
        return UserRepository;
      case 'recommender':
        return RecommenderRepository;
      case 'template':
        return TemplateRepository;
      case 'parameter':
        return ParameterRepository;
      case 'position':
        return PositionRepository;
      case 'candidate':
        return CandidateRepository;
      case 'team':
        return TeamRepository;
      case 'add_cv':
        return AddCvRepository;
      case 'contact_candidate':
        return ContactCandidateRepository;
      case 'mail':
        return MailRepository;
      case 'office':
        return OfficeRepository;
      case 'candidate_confirm':
        return CandidateConfirmRepository;
      case 'candidate_list':
        return CandidateListRepository;
      case 'invite_interview':
        return InviteInterviewRepository;
      case 'candidate_pass_list':
        return CandidatePassListRepository;
      case 'confirm_test':
        return ConfirmTestRepository;
      case 'interview_schedule':
        return InterviewScheduleRepository;
      case 'meeting_room':
        return MeetingRoomRepository;
      case 'black_list':
        return BlackListRepository;
      case 'candidate_assessment':
        return CandidateAssessmentRepository;
      case 'staff_list':
        return StaffListRepository;
      default:
        throw Error('Invalid param');
    }
  }
}

export default new RepositoryFactory();
