import candidateSchema from '../../models/candidate.js';
import { ERROR } from '../../../shared/utilities/message';

const editCandidateSchema = {
  type: 'object',
  required: [
    'fullname',
    'email',
    'birthday',
    'full_address',
    'telephone_no',
    'team_id',
    'position_id',
  ],
  properties: {
    id: {
      type: 'integer',
    },
    fullname: {
      ...candidateSchema.fullname,
      errorMessage: {
        maxLength: ERROR.FULLNAME.MAXLENGTH,
        _: ERROR.FULLNAME.REQUIRED,
      },
    },
    email: {
      ...candidateSchema.email,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    birthday: {
      ...candidateSchema.birthday,
      errorMessage: {
        minLength: ERROR.BIRTHDAY.REQUIRED,
        _: ERROR.BIRTHDAY.INVALID,
        dateMustBeInPast: ERROR.BIRTHDAY.IN_PAST,
      },
    },
    full_address: {
      ...candidateSchema.full_address,
      errorMessage: {
        maxLength: ERROR.FULL_ADDRESS.MAXLENGTH,
        _: ERROR.FULL_ADDRESS.REQUIRED,
      },
    },
    telephone_no: {
      ...candidateSchema.telephone_no,
      errorMessage: {
        minLength: ERROR.TELEPHONE_NO.REQUIRED,
        _: ERROR.TELEPHONE_NO.INVALID,
      },
    },
    team_id: {
      ...candidateSchema.team_id,
      errorMessage: {
        minLength: ERROR.TEAM_ID.REQUIRED,
        _: ERROR.POSITION_ID.INVALID,
      },
    },
    position_id: {
      ...candidateSchema.position_id,
      errorMessage: {
        minLength: ERROR.POSITION_ID.REQUIRED,
        _: ERROR.POSITION_ID.INVALID,
      },
    },
    recommender_id: {
      type: 'string',
    },
    status: {
      type: 'integer',
      minLength: 1,
      errorMessage: {
        minLength: ERROR.STATUS.REQUIRED,
        _: ERROR.STATUS.INVALID,
      },
    },
    note: {
      type: 'string',
      maxLength: 256,
      errorMessage: {
        maxLength: ERROR.NOTE.MAXLENGTH,
        _: ERROR.NOTE.INVALID,
      },
    },
    recommender_name: {
      type: 'string',
    },
    list_interview: {
      type: 'array',
    },
    file_size: {
      type: 'string',
    },
    file_ext: {
      type: 'string',
    },
    file: {
      type: 'string',
    },
  },
  additionalProperties: false,
};

export default editCandidateSchema;
