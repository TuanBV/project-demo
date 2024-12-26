import userModel from 'models/user.js'
// import { ERROR } from '../../../shared/utilities/message'

const addUserSchema = {
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
    },
    birthday: {
      anyOf: [
        { type: 'null' },
        {
          ...userModel.birthday,
          errorMessage: {
            format: 'Invalid birthday.',
            _: 'Invalid birthday'
          }
        }
      ]
    },
    area: {
      ...userModel.area,
      errorMessage: {
        maxLength: 'Max length of area is 256 characters',
        _: 'Invalid area'
      }
    },
    city: {
      ...userModel.city,
      errorMessage: {
        maxLength: 'Max length of city is 256 characters',
        _: 'Invalid city'
      }
    },
    state: {
      ...userModel.state,
      errorMessage: {
        maxLength: 'Max length of state is 256 characters',
        _: 'Invalid state'
      }
    },
    postcode: {
      ...userModel.postcode,
      errorMessage: {
        maxLength: 'Max length of postcode is 10 characters',
        _: 'Invalid postcode'
      }
    }
  },
  additionalProperties: false
}

export default addUserSchema
