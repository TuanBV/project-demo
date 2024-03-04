import { ERROR } from '../../../shared/utilities/message';

const addInterviewSchema = {
  type: 'object',
  required: [
    'employee',
    'date_interview',
    'time_interview',
    'meeting_room',
  ],
  properties: {
    employee: {
      type: 'array',
      minItems: 1,
      errorMessage: {
        minItems: ERROR.INTERVIEWER.MINITEMS,
        _: ERROR.INTERVIEWER.MINITEMS,
      },
    },
    date_interview: {
      type: 'string',
      minLength: 1,
      pattern: '^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$',
      checkDate: true,
      errorMessage: {
        minLength: ERROR.INTERVIEW_DATE.REQUIRED,
        pattern: ERROR.BIRTHDAY.INVALID,
        _: ERROR.INTERVIEW_DATE.INVALID,
        checkDate: ERROR.INTERVIEW_DATE.FAIL_DATE,
      },
    },
    time_interview: {
      type: 'string',
      minLength: 1,
      errorMessage: {
        minLength: ERROR.INTERVIEW_TIME.REQUIRED,
        _: ERROR.INTERVIEW_TIME.INVALID,
      },
    },
    meeting_room: {
      type: 'string',
      minLength: 1,
      errorMessage: {
        minLength: ERROR.MEETING_ROOM.REQUIRED,
        _: ERROR.MEETING_ROOM.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default addInterviewSchema;
