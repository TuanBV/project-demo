import userSchema from 'models/user';
import { ERROR } from 'utilities/message';

const loginSchema = {
  type: 'object',
  required: ['email', 'password'],
  properties: {
    email: {
      ...userSchema.mail,
      errorMessage: {
        maxLength: ERROR.EMAIL.MAXLENGTH,
        minLength: ERROR.EMAIL.REQUIRED,
        _: ERROR.EMAIL.INVALID,
      },
    },
    password: {
      ...userSchema.password,
      errorMessage: {
        minLength: ERROR.PASSWORD.REQUIRED,
        maxLength: ERROR.PASSWORD.MAXLENGTH,
        _: ERROR.PASSWORD.INVALID,
      },
    },
  },
  additionalProperties: false,
};

export default loginSchema;
