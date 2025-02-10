import userModel from 'models/user.js'
// import { ERROR } from '../../../shared/utilities/message'

const userSchema = {
  type: 'object',
  required: ['username', 'fullname', 'email', 'password'],
  properties: {
    username: {
      ...userModel.username,
      errorMessage: {
        maxLength: 'Max length is 256.',
        minLength: 'Username is required to enter.',
        _: 'Invalid username'
      }
    },
    fullname: {
      ...userModel.fullname,
      errorMessage: {
        maxLength: 'Max length is 256.',
        minLength: 'Fullname is required to enter.',
        _: 'Invalid fullname'
      }
    },
    email: {
      ...userModel.email,
      errorMessage: {
        maxLength: 'Max length is 256.',
        minLength: 'Email is required to enter.',
        pattern: 'Invalid email address',
        _: 'Invalid email address'
      }
    },
    password: {
      ...userModel.password,
      errorMessage: {
        minLength: 'Password is required to enter.',
        _: 'Invalid password'
      }
    }
  },
  additionalProperties: false
}

export default userSchema
