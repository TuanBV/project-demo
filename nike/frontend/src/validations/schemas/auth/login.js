import userModel from 'models/user.js'

const loginSchema = {
  type: 'object',
  required: ['email', 'password'],
  properties: {
    email: {
      ...userModel.email,
      errorMessage: {
        maxLength: 'Max length is 256.',
        minLength: 'Email is required to enter.',
        pattern: 'Invalid email address',
        _: 'Invalid email address',
      },
    },
    password: {
      ...userModel.password,
      errorMessage: {
        minLength: 'Password is required to enter.',
        _: 'Invalid password',
      },
    },
  },
  additionalProperties: false,
}

export default loginSchema
