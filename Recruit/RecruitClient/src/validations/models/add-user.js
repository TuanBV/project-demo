const addUserSchema = {
  employee_code: {
    type: 'string',
    maxLength: 6,
    minLength: 1,
  },
  fullname: {
    type: 'string',
    maxLength: 50,
    minLength: 1,
  },
  email: {
    type: 'string',
    minLength: 1,
    maxLength: 256,
    pattern: '^[A-Za-z0-9_!#$%&*+/=?`\'{|}~^.-]+@[A-Za-z0-9.-]+$',
  },
  password: {
    type: 'string',
    minLength: 8,
    pattern: '(?=.{8,})((?=.*\\d)(?=.*[a-z])(?=.*[A-Z])|(?=.*\\d)(?=.*[a-zA-Z])(?=.*[\\W_])|(?=.*[a-z])(?=.*[A-Z])(?=.*[\\W_])).*',
  },
  birthday: {
    type: 'string',
    minLength: 1,
    pattern: '^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$',
    checkDate: true,
    checkBirthday: true,
  },
  registered_date: {
    type: 'string',
    checkDate: true,
    checkBirthday: true,
  },
  full_address: {
    type: 'string',
    minLength: 1,
    maxLength: 256,
  },
  position_id: {
    type: 'string',
    minLength: 1,
  },
  gender: {
    type: 'string',
    minLength: 1,
  },
  office_id: {
    type: 'string',
    minLength: 1,
  },
  place_issued_identification: {
    minLength: 1,
    maxLength: 100,
  },
  identification_number: {
    type: 'string',
    checkIdentificationNumber: true,
    checkRequired: true,
    minLength: 9,
    maxLength: 12,
    pattern: '^[0-9]{12}|[0-9]{9}$',
  },
  date_issued_identification: {
    type: 'string',
    minLength: 1,
    pattern: '^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$',
    checkDate: true,
    checkBirthday: true,
  },
  telephone_no: {
    minLength: 1,
    pattern: '^0(\\d{9,10})$',
  },
};

export default addUserSchema;
