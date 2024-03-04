import candidateSchema from '../../models/candidate.js';
import { ERROR } from '../../../shared/utilities/message';

const addContactSchema = {
  type: 'object',
  required: ['interview_form'],
  properties: {
    date: {},
    time: {},
    office_id: {},
    candidate_id: {},
    link_interview: {},
    note: {},
    interview_form: {
      type: 'string',
      enum: ['1', '2'],
    },
  },
  if: {
    properties: {
      interview_form: {
        enum: ['2'],
      },
    },
  },
  then: {
    required: ['date', 'time', 'office_id', 'link_interview'],
    properties: {
      date: {
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
      time: {
        type: 'string',
        minLength: 1,
        errorMessage: {
          minLength: ERROR.INTERVIEW_TIME.REQUIRED,
          _: ERROR.INTERVIEW_TIME.INVALID,
        },
      },
      office_id: {
        ...candidateSchema.office_id,
        errorMessage: {
          minLength: ERROR.OFFICE_ID.REQUIRED,
          _: ERROR.OFFICE_ID.INVALID,
        },
      },
      candidate_id: {
        type: 'string',
      },
      link_interview: {
        type: 'string',
        minLength: 1,
        errorMessage: {
          minLength: ERROR.LINK_INTERVIEW.REQUIRED,
          _: ERROR.LINK_INTERVIEW.REQUIRED,
        },
      },
      note: {
        type: 'string',
      },
    },
  },
  else: {
    required: ['date', 'time', 'office_id', 'link_interview'],
    properties: {
      date: {
        type: 'string',
        minLength: 1,
        pattern: '^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$',
        checkDate: true,
        errorMessage: {
          minLength: ERROR.INTERVIEW_DATE.REQUIRED,
          pattern: ERROR.BIRTHDAY.INVALID,
          checkDate: ERROR.BIRTHDAY.FAIL_DATE,
          _: ERROR.INTERVIEW_DATE.INVALID,
        },
      },
      time: {
        type: 'string',
        minLength: 1,
        errorMessage: {
          minLength: ERROR.INTERVIEW_TIME.REQUIRED,
          _: ERROR.INTERVIEW_TIME.INVALID,
        },
      },
      office_id: {
        ...candidateSchema.office_id,
        errorMessage: {
          minLength: ERROR.OFFICE_ID.REQUIRED,
          _: ERROR.OFFICE_ID.INVALID,
        },
      },
      candidate_id: {
        type: 'string',
      },
      link_interview: {
        type: 'string',
      },
      note: {
        type: 'string',
      },
    },
  },
  additionalProperties: false,
};

export default addContactSchema;
