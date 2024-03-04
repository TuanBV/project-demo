import candidateModel from 'models/candidate';
import { ERROR } from 'utilities/message';

const formCandidateSchema = {
  type: 'object',
  required: [
    'fullname',
    'birthday',
    'place_of_birth',
    'full_address',
    'identification_number',
    'date_issued_identification',
    'place_issued_identification',
    'bank_account',
    'bank_branch',
    'vehicle_number',
    'telephone_no',
    'start_join_date',
  ],
  properties: {
    fullname: {
      ...candidateModel.fullname,
      errorMessage: {
        maxLength: ERROR.FULLNAME.MAXLENGTH,
        _: ERROR.FULLNAME.REQUIRED,
      },
    },
    birthday: {
      ...candidateModel.birthday,
      errorMessage: {
        minLength: ERROR.BIRTHDAY.REQUIRED,
        dateMustBeInPast: ERROR.BIRTHDAY.IN_PAST,
        _: ERROR.BIRTHDAY.INVALID,
      },
    },
    place_of_birth: {
      ...candidateModel.place_of_birth,
      errorMessage: {
        maxLength: ERROR.PLACE_OF_BIRTH.MAXLENGTH,
        _: ERROR.PLACE_OF_BIRTH.REQUIRED,
      },
    },
    full_address: {
      ...candidateModel.full_address,
      errorMessage: {
        maxLength: ERROR.FULL_ADDRESS.MAXLENGTH,
        _: ERROR.FULL_ADDRESS.REQUIRED,
      },
    },
    identification_number: {
      ...candidateModel.identification_number,
      errorMessage: {
        minLength: ERROR.IDENTIFICATION_NUMBER.REQUIRED,
        _: ERROR.IDENTIFICATION_NUMBER.INVALID,
      },
    },
    date_issued_identification: {
      ...candidateModel.date_issued_identification,
      errorMessage: {
        minLength: ERROR.DATE_ISSUED_IDENTIFICATION.REQUIRED,
        dateMustBeInPast: ERROR.DATE_ISSUED_IDENTIFICATION.IN_PAST,
        _: ERROR.DATE_ISSUED_IDENTIFICATION.INVALID,
      },
    },
    place_issued_identification: {
      ...candidateModel.place_issued_identification,
      errorMessage: {
        maxLength: ERROR.PLACE_ISSUED_IDENTIFICATION.MAXLENGTH,
        _: ERROR.PLACE_ISSUED_IDENTIFICATION.REQUIRED,
      },
    },
    bank_account: {
      ...candidateModel.bank_account,
      errorMessage: {
        maxLength: ERROR.BANK_ACCOUNT.MAXLENGTH,
        pattern: ERROR.BANK_ACCOUNT.INVALID,
        _: ERROR.BANK_ACCOUNT.REQUIRED,
      },
    },
    bank_branch: {
      ...candidateModel.bank_branch,
      errorMessage: {
        maxLength: ERROR.BANK_BRANCH.MAXLENGTH,
        pattern: ERROR.BANK_BRANCH.INVALID,
        _: ERROR.BANK_BRANCH.REQUIRED,
      },
    },
    vehicle_number: {
      ...candidateModel.vehicle_number,
      errorMessage: {
        maxLength: ERROR.VEHICLE_NUMBER.MAXLENGTH,
        pattern: ERROR.VEHICLE_NUMBER.INVALID,
        _: ERROR.VEHICLE_NUMBER.REQUIRED,
      },
    },
    start_join_date: {
      ...candidateModel.start_join_date,
      errorMessage: {
        dateIsFuture: ERROR.START_JOIN_DATE.IS_FUTURE,
        _: ERROR.START_JOIN_DATE.REQUIRED,
      },
    },
    telephone_no: {
      ...candidateModel.telephone_no,
      errorMessage: {
        minLength: ERROR.TELEPHONE_NO.REQUIRED,
        _: ERROR.TELEPHONE_NO.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default formCandidateSchema;
