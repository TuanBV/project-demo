const candidateSchema = {
  fullname: {
    type: 'string',
    maxLength: 50,
    minLength: 1,
  },
  email: {
    type: 'string',
    maxLength: 256,
    minLength: 1,
    pattern: '^[A-Za-z0-9_!#$%&*+/=?`\'{|}~^.-]+@[A-Za-z0-9.-]+$',
  },
  birthday: {
    type: 'string',
    minLength: 1,
    pattern: '^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$',
    dateMustBeInPast: true,
    checkDate: true,
  },
  start_join_date: {
    type: 'string',
    minLength: 1,
    pattern: '^(\\d{4})\\/(0[1-9]|1[0-2])\\/(0[1-9]|[1-2][0-9]|3[0-1])$',
    dateIsFuture: true,
  },
  full_address: {
    type: 'string',
    minLength: 1,
    maxLength: 256,
  },
  telephone_no: {
    type: 'string',
    minLength: 1,
    pattern: '^0(\\d{9,10})$',
  },
  cv_file: {
    type: 'object',
    properties: {
      file_size: {
        type: 'string',
      },
      file_ext: {
        type: 'string',
      },
      file: {
        type: 'string',
        minLength: 1,
        errorMessage: {
          minLength: 'Vui lòng chọn file',
          _: 'Vui lòng chọn file',
        },
      },
    },
  },
  team_id: {
    type: 'string',
    minLength: 1,
  },
  position_id: {
    type: 'string',
    minLength: 1,
  },
  office_id: {
    type: 'string',
    minLength: 1,
  },
  recommender_id: {
    type: 'string',
  },
  place_of_birth: {
    type: 'string',
    minLength: 1,
    maxLength: 256,
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
  place_issued_identification: {
    type: 'string',
    minLength: 1,
    maxLength: 100,
  },
  bank_account: {
    type: 'string',
    maxLength: 50,
    pattern: '^\\d+$|^$',
  },
  bank_branch: {
    type: 'string',
    maxLength: 256,
  },
  vehicle_number: {
    type: 'string',
    maxLength: 9,
    pattern: '^[A-Za-z0-9]+$|^$',
  },
  gender: {
    type: 'string',
    pattern: '^[0-2]$',
  },
  number_experiences: {
    type: 'string',
    minLength: 1,
    pattern: '^\\d{1,5}$|(?=^.{1,5}$)^\\d+\\.\\d{0,1}$',
  },
};

export default candidateSchema;
