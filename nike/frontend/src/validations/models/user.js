const userModel = {
  username: {
    type: 'string',
    maxLength: 256,
    minLength: 1
  },
  fullname: {
    type: 'string',
    maxLength: 256,
    minLength: 1
  },
  email: {
    type: 'string',
    minLength: 1,
    maxLength: 256,
    pattern: "^[A-Za-z0-9_!#$%&*+/=?`'{|}~^.-]+@[A-Za-z0-9.-]+$"
  },
  password: {
    type: 'string',
    minLength: 8,
    pattern:
      '(?=.{8,})((?=.*\\d)(?=.*[a-z])(?=.*[A-Z])|(?=.*\\d)(?=.*[a-zA-Z])(?=.*[\\W_])|(?=.*[a-z])(?=.*[A-Z])(?=.*[\\W_])).*'
  },
  birthday: {
    type: 'string',
    format: 'date'
  },
  area: {
    type: 'string',
    maxLength: 256
  },
  city: {
    type: 'string',
    maxLength: 256
  },
  state: {
    type: 'string',
    maxLength: 256
  },
  postcode: {
    type: 'string',
    maxLength: 10
  }
}

export default userModel
