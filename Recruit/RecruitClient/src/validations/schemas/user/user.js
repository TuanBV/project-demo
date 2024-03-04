import addUserSchema from '../../models/add-user.js';
import { ERROR } from '../../../shared/utilities/message';

const userSchema = {
  type: 'object',
  required: [
    'employee_code',
    'fullname',
    'email',
    'birthday',
    'gender',
    'full_address',
    'position_id',
    'office_id',
    'place_issued_identification',
    'identification_number',
    'date_issued_identification',
    'telephone_no',
  ],
  properties: {
    employee_code: {
      ...addUserSchema.employee_code,
      errorMessage: {
        maxLength: ERROR.EMPLOYEE_CODE.MAXLENGTH,
        minLength: ERROR.EMPLOYEE_CODE.REQUIRED,
        _: ERROR.EMPLOYEE_CODE.REQUIRED,
      },
    },
    fullname: {
      ...addUserSchema.fullname,
      errorMessage: {
        maxLength: ERROR.FULLNAME.MAXLENGTH,
        _: ERROR.FULLNAME.REQUIRED,
      },
    },
    email: {
      ...addUserSchema.email,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    birthday: {
      ...addUserSchema.birthday,
      errorMessage: {
        minLength: ERROR.BIRTHDAY.REQUIRED,
        pattern: ERROR.BIRTHDAY.INVALID,
        checkDate: ERROR.BIRTHDAY.FAIL_DATE,
        checkBirthday: ERROR.BIRTHDAY.IN_PAST,
        _: ERROR.BIRTHDAY.INVALID,
      },
    },
    registered_date: {
      ...addUserSchema.registered_date,
      errorMessage: {
        checkDate: ERROR.REGISTERED_DATE.INVALID,
        checkBirthday: ERROR.BIRTHDAY.IN_PAST,
        _: ERROR.REGISTERED_DATE.INVALID,
      },
    },
    full_address: {
      ...addUserSchema.full_address,
      errorMessage: {
        maxLength: ERROR.FULL_ADDRESS.MAXLENGTH,
        _: ERROR.FULL_ADDRESS.REQUIRED,
      },
    },
    position_id: {
      ...addUserSchema.position_id,
      errorMessage: {
        minLength: ERROR.POSITION_ID.REQUIRED,
        _: ERROR.POSITION_ID.INVALID,
      },
    },
    gender: {
      ...addUserSchema.gender,
      errorMessage: {
        minLength: ERROR.GENDER.REQUIRED,
        _: ERROR.GENDER.INVALID,
      },
    },
    office_id: {
      ...addUserSchema.office_id,
      errorMessage: {
        minLength: ERROR.OFFICE_ID.REQUIRED,
        _: ERROR.OFFICE_ID.INVALID,
      },
    },
    place_issued_identification: {
      ...addUserSchema.place_issued_identification,
      errorMessage: {
        maxLength: ERROR.PLACE_ISSUED_IDENTIFICATION.MAXLENGTH,
        _: ERROR.PLACE_ISSUED_IDENTIFICATION.REQUIRED,
      },
    },
    identification_number: {
      ...addUserSchema.identification_number,
      errorMessage: {
        checkIdentificationNumber: ERROR.IDENTIFICATION_NUMBER.INVALID,
        checkRequired: ERROR.IDENTIFICATION_NUMBER.REQUIRED,
        minLength: ERROR.IDENTIFICATION_NUMBER.MINLENGTH,
        maxLength: ERROR.IDENTIFICATION_NUMBER.MAXLENGTH,
        _: ERROR.IDENTIFICATION_NUMBER.INVALID,
      },
    },
    date_issued_identification: {
      ...addUserSchema.date_issued_identification,
      errorMessage: {
        minLength: ERROR.DATE_ISSUED_IDENTIFICATION.REQUIRED,
        pattern: ERROR.DATE_ISSUED_IDENTIFICATION.INVALID,
        checkDate: ERROR.DATE_ISSUED_IDENTIFICATION.FAIL_DATE,
        checkBirthday: ERROR.DATE_ISSUED_IDENTIFICATION.IN_PAST,
        _: ERROR.DATE_ISSUED_IDENTIFICATION.INVALID,
      },
    },
    telephone_no: {
      ...addUserSchema.telephone_no,
      errorMessage: {
        minLength: ERROR.TELEPHONE_NO.REQUIRED,
        _: ERROR.TELEPHONE_NO.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default userSchema;
