const recommenderSchema = {
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
  birthday: {
    type: 'string',
    minLength: 1,
    pattern: '^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$',
    dateMustBeInPast: true,
  },
  full_address: {
    type: 'string',
    minLength: 1,
    maxLength: 256,
  },
  place_issued_identification: {
    type: 'string',
    minLength: 1,
    maxLength: 100,
  },
  identification_number: {
    type: 'string',
    minLength: 1,
    pattern: '^[0-9]{12}$',
  },
  date_issued_identification: {
    type: 'string',
    minLength: 1,
    pattern: '^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$',
    dateMustBeInPast: true,
  },
  telephone_no: {
    type: 'string',
    minLength: 1,
    pattern: '^0(\\d{9,10})$',
  },
};

export default recommenderSchema;
