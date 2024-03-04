import candidateSchema from '../../models/candidate.js';
import { ERROR } from '../../../shared/utilities/message';

const addCvSchema = {
  type: 'object',
  required: [
    'fullname',
    'email',
    'birthday',
    'full_address',
    'telephone_no',
    'team_id',
    'position_id',
    'office_id',
    'gender',
    'number_experiences',
  ],
  properties: {
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
        pattern: ERROR.BIRTHDAY.INVALID,
        checkDate: ERROR.BIRTHDAY.FAIL_DATE,
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
    cv_file: {
      ...candidateSchema.cv_file,
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
    office_id: {
      ...candidateSchema.office_id,
      errorMessage: {
        minLength: ERROR.OFFICE_ID.REQUIRED,
        _: ERROR.OFFICE_ID.INVALID,
      },
    },
    recommender_id: {
      ...candidateSchema.recommender_id,
    },
    gender: {
      ...candidateSchema.gender,
      errorMessage: {
        _: ERROR.GENDER.INVALID,
      },
    },
    number_experiences: {
      ...candidateSchema.number_experiences,
      errorMessage: {
        minLength: ERROR.EXPERIENCE.REQUIRED,
        pattern: ERROR.EXPERIENCE.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default addCvSchema;
